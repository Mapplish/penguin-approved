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

## Stand 0 (eingestellt 2026-11-22, 10:24)

Start des Abgleichs: alle Kreise offen außer den beiden Schlafzimmer-Kreisen
OG_01 und OG_06. Die Sollwerte sind eine eigene Schätzung als neutraler
Startpunkt: ähnliche Durchflüsse je Etage, Bad als Kandidat für den
Referenzraum großzügig, Büro unverändert. Eric hat alle Kreise eingestellt
und kontrolliert, jeder Ist-Wert entspricht dem Soll. Raumnamen stammen aus
Erics Arbeitsdokument „Heizkreise und Referenzraum“ vom 2026-11-22 (noch
nicht per Rohrverfolgung bestätigt, außer EG_04 = WC). Ab hier wertet
`docs/ABGLEICH.md` jeden Schritt aus. Die Ausgangswerte wurden am
2026-11-22 um 10:24 gespeichert.

| Kreis | Raum | 28.10. | **Stand 0** (l/min) |
|---|---|---|---|
| OG_01 | Schlafzimmer fensterseitig | 0 | **0 (zu)** |
| OG_02 | Büro/Gäste bettseitig | 2,5 | **1,5** |
| OG_03 | Zimmer Weiß | 0,5 | **1,0** |
| OG_04 | Kinderzimmer Velux | 2,5 | **2,5** |
| OG_05 | Büro/Gäste türseitig | 0,5 | **1,5** |
| OG_06 | Schlafzimmer türseitig | 0 | **0 (zu)** |
| OG_07 | Flur | 0 | **1,0** |
| OG_08 | Badezimmer | 2 | **3,0** |
| EG_01 | Wohnzimmer fensterseitig | 1 | **1,5** |
| EG_02 | Esszimmer kaminseitig | 1,6 | **1,5** |
| EG_03 | Wohnzimmer Mitte | 1,6 | **1,5** |
| EG_04 | WC | 0 | **1,0** |
| EG_05 | Esszimmer Mitte | 1,5 | **1,5** |
| EG_06 | Küche | 1 | **1,0** |
| EG_07 | Eingang treppenseitig | 0 | **1,0** |
| EG_08 | Eingang türseitig | 0 | **1,0** |
| EG_09 | Büro | 2,5 | **2,5** |
| UG_01 | Hobbyraum/Werkstatt wandseitig | 0,5 | **0,6** |
| UG_02 | Hobbyraum/Werkstatt Mitte | 0,5 | **0,6** |
| UG_03 | Waschküche | 0,6 | **0,6** |
| UG_04 | Vorrat | 0,6 | **0,6** |
| UG_05 | Diele treppenseitig | 0 | **0,6** |
| UG_06 | Bar | 0,5 | **0,6** |
| UG_07 | WC und Dusche | 0,5 | **0,6** |
| UG_08 | Sauna | 0,6 | **0,6** |
| KA_01/02 | Kaminzimmer (Altkreise) | – | Drehventil unverändert |

Summe: EG 12,5 + OG 10,0 + UG 4,8 = **27,8 l/min** (vorher ≈ 21). Mit den
Kaminkreisen (geschätzt ca. 3 l/min) sind das ≈ 1830 l/h. Das liegt unter
dem WP-Volumenstrom von ≈ 2050–2090 l/h, die Weiche MPS 40 fließt also
weiter in die unkritische Richtung. Grenze: ca. 30 l/min an den Verteilern.

## Schritte nach Stand 0

Jeder Schritt ist genau eine Änderung, bewertet nach 48 h (`docs/ABGLEICH.md`).

| Nr. | Datum | Änderung | Grund | Summe danach |
|---|---|---|---|---|
| 1 | 2026-11-28 | OG_04 Kinderzimmer Velux 2,5 → **2,0** l/min | Raum lag 48 h im Median bei 22,6 °C, nachts bei 23,1 °C und stieg weiter (Ziel 20–22 °C). Der Rücklauf war mit 24,7 °C einer der höchsten (Analyse 21.–28.11.). | OG 9,5 · gesamt 27,3 l/min |

Kontrolle der UG-Kreise am 2026-11-28: Alle Anzeiger stehen auf 0,5–0,6 l/min,
also wie bei Stand 0. Nichts wurde nachgestellt. Der Temperaturabfall im UG
seit Stand 0 kommt also nicht daher, dass sich die Ventile verstellt haben.

Die Tabellen unten zeigen den Stand vom 28.10. und die Beobachtungen davor.

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
