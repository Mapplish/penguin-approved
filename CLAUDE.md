# Penguin Approved – Projektkontext für Claude Code

## Was das Projekt ist
Home-Assistant-basiertes Projekt zur datengetriebenen Optimierung von 
Fußbodenheizung und Wärmepumpe (Vaillant, angebunden über eBUS).
Ziel: kein Cloud-Zwang, keine Abos, nur eigene Daten.

Langfristige Ziele (siehe docs/ARCHITECTURE.md, docs/ROADMAP.md):
- Automatischer hydraulischer Abgleich
- Heizkurvenoptimierung
- Kühloptimierung
- COP-Analyse
- Thermisches Gebäudemodell
- Energieverbrauchsprognose

## Repo-Struktur (Monorepo)
- `configuration.yaml` – MUSS im Root bleiben, HA erwartet diesen Pfad hardcoded
- `blueprints/` – MUSS im Root bleiben, ebenfalls HA-hardcoded, nicht per !include umleitbar
- `homeassistant/` – alles andere HA-Config: automations.yaml, scripts.yaml, 
  scenes.yaml, integrations/, dashboards/ (per !include aus configuration.yaml 
  eingebunden, Pfade sind frei wählbar)
- `ebusd/`, `esphome/`, `hardware/`, `experiments/`, `docs/`, `scripts/` – 
  weitere Projektbereiche, aktuell größtenteils noch leer/in Planung

## Was NICHT versioniert wird (.gitignore)
- `custom_components/` – wird von HACS verwaltet, nicht manuell
- `www/community/` – HACS-installierte Custom Cards (JS-Bundles)
- Datenbanken, Logs, `.storage/`, `secrets.yaml`, Zigbee-Netzwerkdaten

## Deployment-Workflow
- Entwicklung erfolgt LOKAL auf dem PC mit Claude Code
- Home Assistant läuft auf einem Raspberry Pi mit Home Assistant OS 
  (IP: 192.168.178.49, kein direkter Root-Filesystem-Zugriff außer via Add-on)
- SSH-Zugriff läuft über das Add-on "Advanced SSH & Web Terminal" (Port 22)
  - Windows-Hinweis: Win32-OpenSSH hat einen Bug mit -etm MAC-Algorithmen 
    in Kombination mit manchen Ciphern ("Corrupted MAC on input"). 
    Funktionierende Kombi: MACs=umac-128-etm@openssh.com, 
    Ciphers=aes256-gcm@openssh.com (siehe ~/.ssh/config, Host "penguin-pi")
- **Vor jedem Deploy**: `python scripts/check_config.py` lokal laufen lassen
  (prüft YAML-Syntax, doppelte `unique_id`s, und ob selbstdefinierte
  Entity-Referenzen wirklich auf existierende entity_ids zeigen — siehe
  Slugify-Falle unten und `docs/EBUSD_REGISTERS.md`)
- Deploy-Prozess: PC pusht zu GitHub → auf dem Pi per SSH pullen. Das echte
  Arbeitsverzeichnis auf dem Pi ist `/homeassistant`, **nicht** `/config`
  (`.git` gehört root, daher: `sudo git -C /homeassistant pull`; beim
  allerersten Mal zusätzlich `sudo git config --global --add safe.directory
  /homeassistant`)
- Nach Config-Änderungen: `ha core restart` auf dem Pi. Über eine reine
  `ssh host "ha core restart"`-Zeile schlägt das fehl (Supervisor-Token
  fehlt in der Non-Login-Shell) — in eine Login-Shell wrappen:
  `ssh penguin-pi "bash -lc 'ha core restart'"`
- YAML-Mode-Dashboards werden live von der Platte gelesen, kein Restart
  nötig für eine schnelle Preview: Datei per `sudo tee` auf den Pi kopieren,
  Browser neu laden. Achtung CRLF: dieses Repo hat `core.autocrlf=true`,
  beim direkten Kopieren (statt `git pull`) vorher CRLF strippen
  (`sed 's/\r$//'`), sonst meldet ein späteres `git pull` auf dem Pi
  Konflikte wegen reiner Zeilenend-Unterschiede

## Home Assistant MCP-Verbindung
Claude Code ist über die offizielle HA-Integration "Model Context Protocol 
Server" verbunden (Endpoint: http://192.168.178.49:8123/api/mcp, 
Streamable HTTP, Long-Lived Access Token). Damit lassen sich Entity-States 
live abfragen, um z.B. Dashboard-Entities vor dem Einbau zu verifizieren.
Nur Entities, die auf der "Freigegebene Entitäten"-Seite aktiviert sind, 
sind darüber sichtbar.

## Konventionen
- Deutsch für Dashboards/UI-Texte, Englisch für Code-Kommentare/Doku ist okay
- Vor jedem `configuration.yaml`-Edit: Struktur-Constraints oben beachten
- YAML-Mode-Dashboards, kein UI-Editor (damit alles versionierbar bleibt)
- **Entity-Namen ohne Umlaute**, sobald der Sensor von anderen Sensoren/
  Dashboards per entity_id referenziert wird. HAs `slugify()` entfernt
  Umlaut-Punkte (ü→u, ä→a) statt sie zu "ue"/"ae" zu transliterieren —
  `"Wärmepumpe"` wird zu `warmepumpe`, nicht `waermepumpe`. Deutsche
  Anzeige-Namen gehören in die `name:`-Overrides der Dashboard-Cards, nicht
  in den internen Sensornamen. `scripts/check_config.py` prüft das vor
  jedem Deploy automatisch.
- **Lovelace-Dashboard-URL-Pfade brauchen zwingend einen Bindestrich**
  (z.B. `raum-klima`, nicht `raumklima`) — sonst schlägt die komplette
  `lovelace`-Integration fehl und reißt `frontend`/`hacs`/`logbook` mit.
  Auch von `scripts/check_config.py` geprüft.
- **Markdown-Card-Content mit Jinja-Schleifen/Tabellen**: `content: >`
  (gefaltetes YAML) verwandelt Zeilenumbrüche in Leerzeichen — eine
  Markdown-Tabelle landet dann in einer Zeile und rendert nicht. Für
  Templates mit mehrzeiliger Ausgabe `content: |` (literal) nutzen und bei
  Kontrollstrukturen (`{% for %}`, `{% if %}`) explizite Whitespace-Trim-
  Marker (`{%- ... -%}`) setzen, sonst bleibt pro Tag-Zeile eine Leerzeile
  übrig. Vor dem Deploy mit `POST /api/template` (Supervisor-Proxy, siehe
  eBUS-Doku) gegentesten — schneller Feedback-Loop ohne Dashboard-Push.

## eBUS/Vaillant-Wissen
Register-Bedeutungen, Enum-Werte (z.B. `rundatastatuscode` für den
Live-Kompressorstatus) und offene Verifikationspunkte gegen das physische
sensoCOMFORT-Display stehen in `docs/EBUSD_REGISTERS.md`. Beim Entdecken
neuer Register/Enums dort ergänzen, nicht neu recherchieren.