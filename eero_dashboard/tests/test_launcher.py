"""Tests for the eero Home Assistant app launcher."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path
from unittest.mock import Mock


APP_DIRECTORY = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "eero_ha_launcher", APP_DIRECTORY / "launcher.py"
)
assert SPEC and SPEC.loader
launcher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(launcher)


class TestHomeAssistantLauncher(unittest.TestCase):
    def test_reads_options(self) -> None:
        options_file = APP_DIRECTORY / "tests" / "options.test.json"
        options_file.write_text('{"mqtt_enabled": true}', encoding="utf-8")
        try:
            self.assertEqual(launcher.read_options(options_file), {"mqtt_enabled": True})
        finally:
            options_file.unlink(missing_ok=True)

    def test_reads_supervisor_mqtt_service(self) -> None:
        response = Mock()
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        response.read.return_value = json.dumps(
            {
                "result": "ok",
                "data": {
                    "host": "core-mosquitto",
                    "port": 1883,
                    "username": "dashboard",
                    "password": "broker-secret",
                },
            }
        ).encode()
        opener = Mock(return_value=response)

        service = launcher.read_supervisor_mqtt(
            {"SUPERVISOR_TOKEN": "supervisor-secret"}, opener
        )

        self.assertEqual(service["host"], "core-mosquitto")
        self.assertEqual(service["port"], 1883)
        request = opener.call_args.args[0]
        self.assertEqual(
            request.get_header("Authorization"), "Bearer supervisor-secret"
        )

    def test_supervisor_credentials_seed_upstream_environment(self) -> None:
        environment = launcher.build_environment(
            {
                "mqtt_enabled": True,
                "mqtt_broker_host": "",
                "require_local_auth": True,
            },
            {"SUPERVISOR_TOKEN": "secret", "TZ": "America/Toronto"},
            {
                "host": "core-mosquitto",
                "port": 1884,
                "username": "dashboard",
                "password": "broker-secret",
            },
        )

        self.assertEqual(environment["MQTT_BROKER_HOST"], "core-mosquitto")
        self.assertEqual(environment["MQTT_BROKER_PORT"], "1884")
        self.assertEqual(environment["MQTT_USERNAME"], "dashboard")
        self.assertEqual(environment["MQTT_PASSWORD"], "broker-secret")
        self.assertEqual(environment["REQUIRE_LOCAL_AUTH"], "true")
        self.assertEqual(environment["DATA_DIR"], "/data")
        self.assertEqual(environment["TZ"], "America/Toronto")
        self.assertNotIn("SUPERVISOR_TOKEN", environment)

    def test_custom_broker_overrides_supervisor_service(self) -> None:
        environment = launcher.build_environment(
            {
                "mqtt_enabled": True,
                "mqtt_broker_host": "mqtt.example.test",
                "mqtt_broker_port": 1885,
                "mqtt_username": "custom-user",
                "mqtt_password": "custom-password",
            },
            {},
            {
                "host": "core-mosquitto",
                "port": 1883,
                "username": "supervisor-user",
                "password": "supervisor-password",
            },
        )

        self.assertEqual(environment["MQTT_BROKER_HOST"], "mqtt.example.test")
        self.assertEqual(environment["MQTT_BROKER_PORT"], "1885")
        self.assertEqual(environment["MQTT_USERNAME"], "custom-user")
        self.assertEqual(environment["MQTT_PASSWORD"], "custom-password")

    def test_missing_supervisor_service_uses_default_broker_name(self) -> None:
        environment = launcher.build_environment(
            {"mqtt_enabled": True, "mqtt_broker_host": ""}, {}
        )

        self.assertEqual(environment["MQTT_BROKER_HOST"], "core-mosquitto")
        self.assertEqual(environment["MQTT_BROKER_PORT"], "1883")


if __name__ == "__main__":
    unittest.main()
