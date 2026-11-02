# Gamerz32 Home Assistant Apps

This repository is the Home Assistant app catalog for Gamerz32's independently maintained apps. It contains the installable Home Assistant app entries and their build definitions; each app's editable application source is maintained in a separate repository.

## Available apps

### Game Server Manager

Manage Minecraft Java, Bedrock, and cross-play servers from a Home Assistant sidebar dashboard. Create servers, manage worlds and player access, browse mods, plugins, add-ons, and content packs, inspect logs, and configure per-server automation.

- **Application source:** [Game-Server-Manager-HA](https://github.com/Gamerz32/Game-Server-Manager-HA)
- **Home Assistant app:** [game_server_manager](https://github.com/Gamerz32/Gamerz32-HA-Apps/tree/main/game_server_manager)
- **Setup and feature guide:** [game_server_manager/README.md](https://github.com/Gamerz32/Gamerz32-HA-Apps/blob/main/game_server_manager/README.md)
- Supports amd64 and aarch64. The Lenovo ThinkCentre M720q uses amd64.

The app uses the Docker API to create and manage game-server containers. Home Assistant requires Docker API access for the app, and Protection mode must be turned off. This grants the app control over host containers; review the setup guide before enabling it. See the [Game Server Manager security policy](https://github.com/Gamerz32/Game-Server-Manager-HA/blob/main/SECURITY.md) for private vulnerability reporting.

### eero Dashboard

View eero WAN throughput, network health, connected clients, mesh nodes, bufferbloat, cloud status, and device presence. MQTT discovery publishes telemetry as Home Assistant entities.

- **Application source:** [Dashboard_EERO-HA](https://github.com/Gamerz32/Dashboard_EERO-HA)
- **Home Assistant app:** [eero_dashboard](https://github.com/Gamerz32/Gamerz32-HA-Apps/tree/main/eero_dashboard)
- **Setup and credential guide:** [eero_dashboard/README.md](https://github.com/Gamerz32/Gamerz32-HA-Apps/blob/main/eero_dashboard/README.md)
- Supports amd64 and aarch64 and opens in the Home Assistant sidebar through ingress.

eero sign-in supports the Amazon account linked to eero and email/SMS verification when enabled for the account. Amazon credentials are entered only on Amazon's sign-in page. MQTT entities require a Home Assistant MQTT broker and integration.

## Install the apps

1. In Home Assistant, open **Settings → Apps → App Store → Repositories**.
2. Add this repository: https://github.com/Gamerz32/Gamerz32-HA-Apps
3. Refresh the app store.
4. Install and start **Game Server Manager**, **eero Dashboard**, or both. Each is a separate Home Assistant app with its own configuration and data.

## Edit and update app source

Edit each app in its own source repository. The app-store Dockerfiles download the source repository's main branch when Home Assistant builds the app.

After changing source, bump that app's version in its configuration file in this repository, then update the app in Home Assistant to trigger a rebuild:

- Game Server Manager: game_server_manager/config.yaml
- eero Dashboard: eero_dashboard/config.yaml

The Home Assistant host needs internet access to GitHub and Python package indexes during an app build. No Docker Hub credentials are needed.

## References and licenses

- [Home Assistant app documentation](https://developers.home-assistant.io/docs/apps/)
- [Home Assistant app security guidance](https://developers.home-assistant.io/docs/apps/guides/security/)
- Game Server Manager is distributed under the repository's [MIT license](https://github.com/Gamerz32/Gamerz32-HA-Apps/blob/main/LICENSE).
- The eero Dashboard attribution and license are documented in [Dashboard_EERO-HA](https://github.com/Gamerz32/Dashboard_EERO-HA).

This community project is not affiliated with Home Assistant, eero, Amazon, Minecraft, Mojang, Microsoft, Modrinth, CurseForge, or the owners of those names and marks.
