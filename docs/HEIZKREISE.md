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

## Erste Ablesung 2026-10-28

Durchflussmesser am Verteiler. Ein Wert von 0 bedeutet: die
Rücklaufverschraubung ist zu. Das wurde irgendwann bewusst so eingestellt und
ist der Ausgangspunkt für den Abgleich.

| Strang | Kreise | offen | Summe (l/min) |
|---|---|---|---|
| EG | 9 | 6 | 9,2 |
| OG | 8 | 5 | 8,0 |
| UG | 8 | 7 | 3,8 |
| **Gesamt** | 25 | 18 | **≈ 21 (≈ 1,25 m³/h)** |

## EG

| Kreis | Raum | Durchfluss (l/min) | Stellantrieb | Stand | Notiz |
|---|---|---|---|---|---|
| EG_01 | ? | 1 |  | 2026-10-28 |  |
| EG_02 | ? | 1,6 |  | 2026-10-28 |  |
| EG_03 | ? | 1,6 |  | 2026-10-28 |  |
| EG_04 | Gäste-WC | 0 | zu | 2026-10-28 | Rücklaufventil zu (bewusst so eingestellt). Raum hält trotzdem 20,5–21 °C (Nachbarräume heizen mit) |
| EG_05 | ? | 1,5 |  | 2026-10-28 |  |
| EG_06 | ? | 1 |  | 2026-10-28 |  |
| EG_07 | ? | 0 |  | 2026-10-28 | Rücklaufventil zu (bewusst so eingestellt). Rücklaufsensor reagiert trotzdem auf Heizläufe (+0,8 K) → Wärme von außen, nicht Durchfluss |
| EG_08 | ? | 0 |  | 2026-10-28 | Rücklaufventil zu (bewusst so eingestellt). Rücklaufsensor reagiert trotzdem leicht (+0,5 K) → Wärme von außen, nicht Durchfluss |
| EG_09 | Büro (vermutet) | 2,5 | auf | 2026-10-28 | Stärkste/schnellste Reaktion aller EG-Kreise; Büro soll bewusst schnell warm werden — beim Abgleich nicht ungefragt drosseln |

## OG

Rücklaufsensoren konfiguriert, noch nicht verdrahtet.

| Kreis | Raum | Durchfluss (l/min) | Stellantrieb | Stand | Notiz |
|---|---|---|---|---|---|
| OG_01 | ? | 0 |  | 2026-10-28 | Rücklaufventil zu (bewusst so eingestellt). |
| OG_02 | ? | 2,5 |  | 2026-10-28 |  |
| OG_03 | ? | 0,5 |  | 2026-10-28 |  |
| OG_04 | ? | 2,5 |  | 2026-10-28 |  |
| OG_05 | ? | 0,5 |  | 2026-10-28 |  |
| OG_06 | ? | 0 |  | 2026-10-28 | Rücklaufventil zu (bewusst so eingestellt). |
| OG_07 | ? | 0 |  | 2026-10-28 | Rücklaufventil zu (bewusst so eingestellt). |
| OG_08 | ? | 2 |  | 2026-10-28 |  |

## UG

Rücklaufsensoren konfiguriert, noch nicht verdrahtet.

| Kreis | Raum | Durchfluss (l/min) | Stellantrieb | Stand | Notiz |
|---|---|---|---|---|---|
| UG_01 | ? | 0,5 |  | 2026-10-28 |  |
| UG_02 | ? | 0,5 |  | 2026-10-28 |  |
| UG_03 | ? | 0,6 |  | 2026-10-28 |  |
| UG_04 | ? | 0,6 |  | 2026-10-28 |  |
| UG_05 | ? | 0 |  | 2026-10-28 | Rücklaufventil zu (bewusst so eingestellt). |
| UG_06 | ? | 0,5 |  | 2026-10-28 |  |
| UG_07 | ? | 0,5 |  | 2026-10-28 |  |
| UG_08 | ? | 0,6 |  | 2026-10-28 |  |

## Kaminraum (separate Altkreise)

Zwei ältere Kreise für den Kaminraum, nicht an den drei Verteilern oben und
ohne Durchflussmesser. Sie lassen sich nur per Drehventil einstellen, der
Durchfluss ist nicht messbar. Hydraulisch liegen sie am nächsten an der
Wärmepumpe und bekommen deshalb immer als erste warmes Wasser. Beim Abgleich
heißt das: Sie werden vermutlich bevorzugt und überversorgt und können den
übrigen Kreisen Durchfluss wegnehmen. Bewerten lassen sie sich nur indirekt,
über die Raumtemperatur im Kaminraum bzw. die Summe aller Durchflüsse im
Vergleich zum WP-Volumenstrom.

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
