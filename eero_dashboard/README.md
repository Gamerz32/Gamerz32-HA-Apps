# eero Dashboard for Home Assistant OS

This Home Assistant app runs Enrico Flammini's existing eero Dashboard as a Supervisor-managed app. It keeps the upstream web interface, SQLite history, eero sign-in flow, and Home Assistant MQTT discovery. The adaptation packages the existing dashboard; it does not duplicate its telemetry in a separate custom integration.

## Install on Home Assistant OS

This add-on is included in the **Gamerz32 Home Assistant Apps** repository. After the change is merged to its `main` branch:

1. In Home Assistant, open **Settings → Apps → App Store** and refresh the store from its menu.
2. Install **eero Dashboard** from this repository and review its **Configuration** tab. HAOS builds this app from its `Dockerfile` and pulls the upstream image from Docker Hub, so the HA host needs internet access for the initial build.
3. If the official Mosquitto Broker app is installed and the MQTT integration is configured, leave **MQTT broker host** blank. The app asks the Supervisor for the broker host, port, and credentials. For another broker, enter its host and a dedicated username/password.
4. Start the app and select **Open Web UI**. The port maps to **8085** on the Home Assistant host by default.
5. Create a local dashboard administrator in the first-run setup screen unless you supplied an administrator password in the app configuration. Sign in to eero and complete its email or SMS verification.

If this repository is not already in the Home Assistant App Store, add `https://github.com/Gamerz32/Game-Server-Manager-HA` under **Repositories** first. For local development, copy the complete `eero_dashboard` folder to `/local_apps/eero_dashboard` (the Samba share exposes a `local_apps` folder; over SSH use `/local_apps/eero_dashboard`), then install it from **Local apps**.

## Home Assistant entities

The dashboard publishes retained MQTT discovery configuration under the configured discovery prefix. Once the Home Assistant MQTT integration is connected to the same broker, the **eero Mesh System** device appears automatically. Discovered entities include WAN download/upload, network health, connected clients, online mesh nodes, bufferbloat grade, internet/cloud status, and per-device presence trackers (up to 250 devices).

No manual `configuration.yaml` sensor definitions or Lovelace card are required. Add the discovered entities to any Home Assistant dashboard using its normal cards.

## Configuration, credentials, and storage

- The app targets Home Assistant OS on `amd64` and `aarch64`; the Lenovo ThinkCentre M720q is `amd64`.
- eero authentication uses the upstream private eero cloud API. Normally you sign in through the dashboard and complete eero's email/SMS one-time code. The resulting session is stored under `/data`, which Home Assistant includes in app backups. An existing `EERO_USER_TOKEN` and a specific `EERO_NETWORK_ID` are optional.
- The Home Assistant app has its own local administrator. **Require local authentication** is enabled by default because the web UI uses a direct host port rather than Home Assistant ingress.
- Home Assistant's timezone is inherited by the app. The interface language defaults to English; Italian is also available.
- MQTT settings can also be changed in the dashboard's **Automations & Controls** panel. Those runtime settings are stored in the app database and may take precedence over startup defaults from the app configuration.
- The current frontend uses root-relative URLs, so this package exposes port 8085 and provides an **Open Web UI** button instead of enabling ingress. If that port is already in use, change `8000/tcp` in this app's `config.yaml` and rebuild it.
- The upstream MQTT discovery payload currently links its device configuration to `http://localhost:8000`. This does not affect telemetry or entity discovery, but that link may not open the dashboard from Home Assistant.
- This app uses the upstream Docker Hub multi-architecture image as its base. The app package version should be updated alongside upstream releases so the Supervisor rebuilds it with the newer base image.

## Upstream and attribution

The dashboard application, eero client, MQTT implementation, UI, and original installation instructions remain from [EnricoFlammini/Dashboard_EERO](https://github.com/EnricoFlammini/Dashboard_EERO). The Home Assistant package is an adaptation under the upstream repository's MIT license. eero is an Amazon brand; this project is an independent community project and is not an official eero or Amazon integration.

---

# eero Dashboard per Home Assistant OS

Questa app di Home Assistant esegue la dashboard eero esistente di Enrico Flammini come app gestita da Supervisor. Mantiene l'interfaccia web originale, lo storico SQLite, l'accesso eero e il rilevamento automatico Home Assistant tramite MQTT. L'adattamento confeziona la dashboard esistente senza duplicarne la telemetria in un'integrazione personalizzata separata.

## Installazione su Home Assistant OS

Questa app è inclusa nel repository **Gamerz32 Home Assistant Apps**. Dopo aver integrato la modifica nel branch `main`:

1. In Home Assistant apri **Impostazioni → App → App store** e aggiorna lo store dal menu.
2. Installa **eero Dashboard** da questo repository e controlla la scheda **Configurazione**. HAOS compila l'app dal `Dockerfile` e scarica l'immagine upstream da Docker Hub; l'host HA deve avere accesso a Internet per la prima compilazione.
3. Se Mosquitto Broker ufficiale è installato e l'integrazione MQTT è configurata, lascia vuoto **Host broker MQTT**. L'app chiede a Supervisor host, porta e credenziali del broker. Per un altro broker, inserisci host e credenziali dedicate.
4. Avvia l'app e scegli **Apri interfaccia web**. Per impostazione predefinita la porta 8000 del container è esposta sulla porta **8085** dell'host Home Assistant.
5. Crea un amministratore locale della dashboard dalla schermata iniziale, a meno che tu abbia già impostato una password nella configurazione dell'app. Accedi a eero e completa la verifica via email o SMS.

Se questo repository non è ancora nell'App store di Home Assistant, aggiungi prima `https://github.com/Gamerz32/Game-Server-Manager-HA` in **Repository**. Per lo sviluppo locale, copia l'intera cartella `eero_dashboard` in `/local_apps/eero_dashboard` (la condivisione Samba mostra la cartella `local_apps`; via SSH usa `/local_apps/eero_dashboard`), quindi installala da **App locali**.

## Entità Home Assistant

La dashboard pubblica la configurazione MQTT discovery retained con il prefisso configurato. Quando l'integrazione MQTT di Home Assistant è collegata allo stesso broker, viene rilevato automaticamente il dispositivo **eero Mesh System**. Le entità includono download/upload WAN, stato della rete, client connessi, nodi mesh online, bufferbloat, stato internet/cloud e tracker di presenza per dispositivo (fino a 250 dispositivi).

Non servono sensori manuali in `configuration.yaml` né una scheda Lovelace dedicata. Aggiungi le entità rilevate a qualsiasi dashboard usando le normali schede Home Assistant.

## Configurazione, credenziali e dati

- L'app supporta Home Assistant OS su `amd64` e `aarch64`; il Lenovo ThinkCentre M720q usa `amd64`.
- L'autenticazione eero usa l'API cloud privata eero già usata dal progetto originale. Normalmente si accede dalla dashboard e si completa il codice temporaneo via email/SMS. La sessione viene salvata in `/data`, inclusa nei backup delle app di Home Assistant. `EERO_USER_TOKEN` e `EERO_NETWORK_ID` sono facoltativi.
- L'app usa un amministratore locale della dashboard. **Richiedi autenticazione locale** è attivo per impostazione predefinita perché l'interfaccia è esposta su una porta host diretta e non tramite ingress di Home Assistant.
- Il fuso orario viene ereditato da Home Assistant. La lingua predefinita è inglese; è disponibile anche l'italiano.
- MQTT si può configurare anche nel pannello **Automazioni e Controlli** della dashboard. Le impostazioni runtime vengono salvate nel database dell'app e possono prevalere sui valori iniziali della configurazione dell'app.
- Il frontend usa URL relativi alla radice, quindi il pacchetto espone la porta 8085 e offre **Apri interfaccia web** invece di abilitare ingress. Se la porta è occupata, cambia `8000/tcp` in `config.yaml` e ricostruisci l'app.
- Attualmente il payload MQTT upstream collega il dispositivo all'URL `http://localhost:8000`. Telemetria e rilevamento delle entità funzionano comunque, ma il collegamento potrebbe non aprire la dashboard da Home Assistant.
- Il pacchetto usa come base l'immagine multi-architettura upstream su Docker Hub. Aggiorna la versione dell'app insieme alle release upstream affinché Supervisor la ricostruisca con l'immagine base più recente.

## Progetto originale e attribuzione

L'applicazione, il client eero, l'implementazione MQTT, l'interfaccia e le istruzioni originali restano opera di [EnricoFlammini/Dashboard_EERO](https://github.com/EnricoFlammini/Dashboard_EERO). Il pacchetto Home Assistant è un adattamento distribuito con la licenza MIT del progetto upstream. eero è un marchio Amazon; questo è un progetto community indipendente, non un'integrazione ufficiale di eero o Amazon.
