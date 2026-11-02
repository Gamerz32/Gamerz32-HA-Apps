# eero Dashboard for Home Assistant

This Home Assistant app packages the dashboard source from [Gamerz32/Dashboard_EERO-HA](https://github.com/Gamerz32/Dashboard_EERO-HA), making it available from the **Gamerz32 Home Assistant Apps** repository.

## Install

1. In Home Assistant, open **Settings → Apps → App Store → Repositories**.
2. Add `https://github.com/Gamerz32/Gamerz32-HA-Apps` if it is not already listed.
3. Refresh the app store, install **eero Dashboard**, and start it.
4. Open **eero Dashboard** from the Home Assistant sidebar.

The package supports `amd64` and `aarch64`. The Lenovo ThinkCentre M720q uses the supported `amd64` architecture. The app uses Home Assistant ingress, so it does not need a host port or a separate Lovelace panel.

## Source updates and editing

The dashboard application is cloned from the `main` branch of [Dashboard_EERO-HA](https://github.com/Gamerz32/Dashboard_EERO-HA) during the Home Assistant image build. The package in this repository contains the Home Assistant app metadata, Docker build, and launcher. It does not copy the dashboard source code.

After changing the source repository, bump the `version` in `eero_dashboard/config.yaml` in this repository and update the app in Home Assistant. The version bump makes Home Assistant rebuild the image with the new source. Home Assistant needs outbound access to GitHub and Python package indexes when it builds the app. No Docker Hub or registry credentials are needed.

## First run and eero sign-in

Home Assistant ingress handles access authentication. The dashboard's own local login is off by default; enable **Require dashboard login** in app options if you want an additional login. Sign in with the Amazon account already linked to eero, or use email/SMS verification if your account supports it. If eero rejects an email/SMS request with `error.login.unknown`, the dashboard automatically opens the Amazon sign-in flow. For Amazon sign-in, open Amazon from the dashboard, sign in on Amazon, then copy the full address shown after Amazon returns and paste it back into the dashboard. Your Amazon password is entered only on Amazon. The dashboard sends the short-lived, one-use authorization code to Amazon and eero to create the eero session, then clears it. The optional eero token and network ID are for advanced setups; most users can leave them blank.

The app stores its database, eero session, logs, and history under its persistent `/data` directory, which is included in Home Assistant app backups.

## MQTT entities

The app requests the Home Assistant MQTT service. If a broker such as Mosquitto is available, the app uses its connection details and publishes Home Assistant MQTT discovery entities. Enable the Home Assistant MQTT integration as well. If there is no Supervisor MQTT service, configure a broker host and credentials in the app options. MQTT publishing does not support TLS brokers.

## Attribution

The dashboard application is based on Enrico Flammini's [eero Custom Dashboard & Mesh Management Suite](https://github.com/EnricoFlammini/Dashboard_EERO), distributed under its MIT license. [Dashboard_EERO-HA](https://github.com/Gamerz32/Dashboard_EERO-HA) maintains the Home Assistant adaptation and source. This repository supplies an installable Home Assistant app entry for it. This is an independent community project and is not affiliated with eero or Amazon.

---

# eero Dashboard per Home Assistant

Questa app Home Assistant usa il codice sorgente di [Dashboard_EERO-HA](https://github.com/Gamerz32/Dashboard_EERO-HA) ed è disponibile nel repository **Gamerz32 Home Assistant Apps**.

## Installazione

1. In Home Assistant, apri **Impostazioni → App → App Store → Repository**.
2. Aggiungi `https://github.com/Gamerz32/Gamerz32-HA-Apps` se non è già presente.
3. Aggiorna l'App Store, installa **eero Dashboard** e avviala.
4. Apri **eero Dashboard** dalla barra laterale di Home Assistant.

L'app supporta `amd64` e `aarch64`. Lenovo ThinkCentre M720q usa l'architettura `amd64`. Home Assistant ingress gestisce l'accesso dalla barra laterale senza esporre una porta sull'host.

## Aggiornare il codice sorgente

Durante la compilazione dell'immagine, il Dockerfile scarica il ramo `main` di [Dashboard_EERO-HA](https://github.com/Gamerz32/Dashboard_EERO-HA). Dopo una modifica al codice sorgente, aggiorna la versione in `eero_dashboard/config.yaml` in questo repository e aggiorna l'app in Home Assistant per ricompilare l'immagine. Home Assistant deve poter accedere a GitHub e agli indici dei pacchetti Python. Non servono credenziali Docker Hub.

## Accesso, MQTT e attribuzione

Accedi a eero dalla dashboard e completa la verifica via email o SMS. L'app usa il servizio MQTT di Home Assistant quando disponibile e pubblica sensori tramite MQTT discovery. I dati persistenti sono salvati in `/data`.

L'applicazione deriva dal progetto di Enrico Flammini [Dashboard_EERO](https://github.com/EnricoFlammini/Dashboard_EERO), distribuito con licenza MIT. [Dashboard_EERO-HA](https://github.com/Gamerz32/Dashboard_EERO-HA) mantiene la versione Home Assistant. Questo repository aggiunge il pacchetto installabile tramite App Store.
