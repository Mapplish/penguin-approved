# Heizkreise

Zuordnung der Fußbodenheizkreise zu Räumen, eingestellte Durchflüsse und
Beobachtungen aus den Rücklaufsensoren. Grundlage für den hydraulischen
Abgleich (siehe ROADMAP.md).

Rücklaufsensoren: ESPHome `esp-verteiler-hobbyraum`, Entities
`sensor.esp_verteiler_hobbyraum_<eg|og|ug>_NN_ruecklauf`. Die Klarnamen
stehen zusätzlich als `# Klarname:`-Kommentar in
`esphome/esp-verteiler-hobbyraum.yaml`.

## Durchflüsse ablesen

- Nur im Heizbetrieb ablesen (`sensor.heating_ebusd_hmu_status01_pumpstate`
  = `on`), nicht während Warmwasser (`hwc`) oder Taktpause.
- Alle Kreise in einem Rutsch ablesen; ein öffnender/schließender
  Stellantrieb verschiebt die Werte der anderen Kreise.
- Mitnotieren, welche Stellantriebe gerade zu sind.

## EG

| Kreis | Raum | Durchfluss (l/min) | Stellantrieb | Stand | Notiz |
|---|---|---|---|---|---|
| EG_01 | ? | | | | |
| EG_02 | ? | | | | |
| EG_03 | ? | | | | |
| EG_04 | Gäste-WC | | zu | 2026-10-27 | Raum hält trotzdem 20,5–21 °C (Nachbarräume heizen mit) |
| EG_05 | ? | | | | |
| EG_06 | ? | | | | |
| EG_07 | ? | | | | |
| EG_08 | ? | | | | |
| EG_09 | Büro (vermutet) | | auf | 2026-10-27 | Stärkste/schnellste Reaktion aller EG-Kreise; Büro soll bewusst schnell warm werden — beim Abgleich nicht ungefragt drosseln |

## OG

Sensoren konfiguriert, noch nicht verdrahtet.

## UG

Sensoren konfiguriert, noch nicht verdrahtet.

## Beobachtungen aus den Rücklaufsensoren

Auswertung 2026-10-24 → 2026-10-27 (EG, Außentemperatur 10,5–13 °C):

- **Absolutwerte unbrauchbar, nur Dynamik nutzbar.** Ohne Durchfluss liegen
  alle EG-Sensoren bei ~17 °C (Luft am Verteiler), im Dauerheizen bei nur
  18–21,5 °C bei ~28 °C WP-Rücklauf — also unter der Raumtemperatur. Die
  Clamp-on-Sensoren auf dem Kunststoffrohr sehen nur ~10–40 % des
  Wassersignals. Der Fehler skaliert mit (Wasser − Umgebung), daher eher
  Gain-Kalibrierung als fester Offset. Vorher: Sensoren mit Armaflex
  isolieren.
- **Reaktion auf einen langen Heizlauf** (So 25.10. 18:05, ~100 min):
  EG_09 +2,3 K innerhalb von Minuten; EG_03 +1,2; EG_02/05 +0,9; EG_07
  +0,8; EG_01/06/08 +0,5–0,6; EG_04 ±0 (Antrieb zu).
- **Warmwasser-Bereitung:** Bei jeder `hwc`-Phase steigen EG_04/06/07/08 um
  0,5–1 K, EG_03/09 fallen. Da EG_04 zu ist (kein Durchfluss), vermutlich
  Wärmeeintrag von einer nahen Warmwasserleitung; Leitungsführung unbekannt,
  wird beobachtet. In Auswertungen dieser vier Kreise `hwc`-Phasen plus ein
  paar Minuten danach ausblenden.
