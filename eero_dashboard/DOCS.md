# eero Dashboard

Open the app from the Home Assistant sidebar. Home Assistant ingress handles authentication and keeps the dashboard inside Home Assistant.

The application source is cloned from https://github.com/Gamerz32/Dashboard_EERO-HA during the image build. To bring source changes into an installed app, increase the version in this repository's `eero_dashboard/config.yaml` and update the app.

Sign in to eero in the dashboard and complete any requested email or SMS verification. The app stores its database and session in `/data`.

When the Home Assistant MQTT service is available, the app uses its credentials and publishes MQTT discovery entities. Otherwise, configure a broker host and credentials in the app options. The MQTT client does not support TLS brokers.
