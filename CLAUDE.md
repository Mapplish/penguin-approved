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
- Deploy-Prozess: PC pusht zu GitHub → auf dem Pi per SSH `cd /config && git pull`
- Nach Config-Änderungen: `ha core restart` auf dem Pi

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