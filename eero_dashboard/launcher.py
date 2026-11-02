"""Home Assistant app launcher for the upstream eero Dashboard image."""

from __future__ import annotations

import json
import os
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Mapping


OPTIONS_FILE = Path("/data/options.json")
DATA_DIRECTORY = "/data"
DATA_PATH = Path(DATA_DIRECTORY)
APP_UID = 10001
APP_GID = 10001

OPTION_ENVIRONMENT = {
    "dashboard_lang": "DASHBOARD_LANG",
    "demo_mode": "DEMO_MODE",
    "poll_interval": "POLL_INTERVAL",
    "history_retention_days": "HISTORY_RETENTION_DAYS",
    "speedtest_interval_hours": "SPEEDTEST_INTERVAL_HOURS",
    "api_docs": "API_DOCS",
    "require_local_auth": "REQUIRE_LOCAL_AUTH",
    "eero_user_token": "EERO_USER_TOKEN",
    "eero_network_id": "EERO_NETWORK_ID",
    "admin_user": "ADMIN_USER",
    "admin_password": "ADMIN_PASSWORD",
    "mqtt_enabled": "MQTT_ENABLED",
    "mqtt_broker_host": "MQTT_BROKER_HOST",
    "mqtt_broker_port": "MQTT_BROKER_PORT",
    "mqtt_username": "MQTT_USERNAME",
    "mqtt_password": "MQTT_PASSWORD",
    "mqtt_base_topic": "MQTT_BASE_TOPIC",
    "mqtt_discovery_prefix": "MQTT_HA_DISCOVERY_PREFIX",
    "mqtt_discovery_enabled": "MQTT_DISCOVERY_ENABLED",
    "mqtt_publish_interval": "MQTT_PUBLISH_INTERVAL",
}

BOOLEAN_OPTIONS = {
    "demo_mode",
    "api_docs",
    "require_local_auth",
    "mqtt_enabled",
    "mqtt_discovery_enabled",
}


def read_options(path: Path = OPTIONS_FILE) -> dict[str, Any]:
    """Read the options written by Home Assistant Supervisor."""
    try:
        options = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except (OSError, json.JSONDecodeError) as err:
        raise RuntimeError("Unable to read /data/options.json") from err

    if not isinstance(options, dict):
        raise RuntimeError("Home Assistant options must be a JSON object")
    return options


def read_supervisor_mqtt(
    environ: Mapping[str, str], open_url: Any = None
) -> dict[str, Any] | None:
    """Get broker connection details shared by the Home Assistant Supervisor."""
    token = environ.get("SUPERVISOR_TOKEN")
    if not token:
        return None

    endpoint = environ.get("SUPERVISOR_ENDPOINT", "http://supervisor").rstrip("/")
    request = urllib.request.Request(
        f"{endpoint}/services/mqtt",
        headers={"Authorization": f"Bearer {token}"},
    )
    opener = open_url or urllib.request.urlopen

    try:
        with opener(request, timeout=3) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (OSError, urllib.error.URLError, TimeoutError, ValueError):
        return None

    if not isinstance(payload, dict):
        return None
    data = payload.get("data", payload)
    return data if isinstance(data, dict) else None


def _as_environment_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def build_environment(
    options: Mapping[str, Any],
    base_environment: Mapping[str, str] | None = None,
    mqtt_service: Mapping[str, Any] | None = None,
) -> dict[str, str]:
    """Translate app options into environment variables consumed upstream."""
    environment = dict(base_environment if base_environment is not None else os.environ)
    environment["DATA_DIR"] = DATA_DIRECTORY

    for option, variable in OPTION_ENVIRONMENT.items():
        if option in options and options[option] is not None:
            value = options[option]
            environment[variable] = (
                _as_environment_value(value)
                if option in BOOLEAN_OPTIONS
                else str(value)
            )

    if options.get("mqtt_enabled", True):
        configured_host = str(options.get("mqtt_broker_host", "")).strip()
        service = mqtt_service if isinstance(mqtt_service, Mapping) else {}

        if configured_host:
            broker_host = configured_host
            broker_port = options.get("mqtt_broker_port", 1883)
            username = options.get("mqtt_username", "")
            password = options.get("mqtt_password", "")
        else:
            broker_host = service.get("host") or "core-mosquitto"
            broker_port = service.get("port") or options.get("mqtt_broker_port", 1883)
            username = options.get("mqtt_username") or service.get("username", "")
            password = options.get("mqtt_password") or service.get("password", "")

        environment["MQTT_BROKER_HOST"] = str(broker_host)
        environment["MQTT_BROKER_PORT"] = str(broker_port)
        environment["MQTT_USERNAME"] = str(username or "")
        environment["MQTT_PASSWORD"] = str(password or "")

    # Do not pass the Supervisor API credential into the web application.
    environment.pop("SUPERVISOR_TOKEN", None)
    environment.pop("HASSIO_TOKEN", None)
    environment.pop("SUPERVISOR_ENDPOINT", None)
    return environment


def prepare_data_directory() -> None:
    """Give the upstream non-root application user access to persistent data."""
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    if os.geteuid() != 0:
        return

    os.chown(DATA_PATH, APP_UID, APP_GID)
    for root, directories, files in os.walk(DATA_PATH, followlinks=False):
        for name in directories + files:
            path = Path(root, name)
            if path == OPTIONS_FILE or path.is_symlink():
                continue
            os.chown(path, APP_UID, APP_GID)


def main(command: list[str] | None = None) -> None:
    """Prepare runtime config and replace this process with the web server."""
    options = read_options()
    mqtt_service = None
    if options.get("mqtt_enabled", True) and not str(
        options.get("mqtt_broker_host", "")
    ).strip():
        mqtt_service = read_supervisor_mqtt(os.environ)
        if mqtt_service is None:
            print(
                "Home Assistant MQTT service was not available; using the configured broker options.",
                file=sys.stderr,
            )

    prepare_data_directory()
    environment = build_environment(options, mqtt_service=mqtt_service)
    process = command or sys.argv[1:]
    if not process:
        process = [
            "uvicorn",
            "app.main:app",
            "--host",
            "0.0.0.0",
            "--port",
            "8000",
            "--workers",
            "1",
            "--log-level",
            "info",
        ]

    su_exec = shutil.which("su-exec")
    if os.geteuid() == 0 and su_exec:
        process = [su_exec, "appuser", *process]
    os.execvpe(process[0], process, environment)


if __name__ == "__main__":
    main()
