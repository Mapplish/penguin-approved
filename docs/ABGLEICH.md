# Abgleich – automatische Auswertung

Home Assistant wertet jeden Abgleich-Schritt nach festen Regeln aus und
schickt das Ergebnis per E-Mail. **Es steuert nichts**: Jede Änderung an
Verteiler oder Regler macht Eric von Hand. Die Auswertung liefert die
Fakten, die Entscheidung bleibt beim Menschen.

Konfiguration: `homeassistant/packages/abgleich.yaml` (Logik, Mails) und
`homeassistant/packages/abgleich_statistik.yaml` (Statistik-Sensoren).
Bedienung: Dashboard „Wärmepumpe“ → Ansicht „Abgleich“.

## Ablauf eines Schritts

1. Genau **eine** Änderung am Verteiler machen.
2. Im Dashboard „Was wurde geändert?“ ausfüllen und den Zielraum wählen.
3. „Schritt gestartet“ drücken. HA speichert die Werte der letzten 48 h
   als Ausgangswerte.
4. 48 h später kommt die Bewertungs-Mail: 48 h vorher gegen 48 h nachher.
5. Zusätzlich kommt jeden Morgen um 07:00 ein Tagesbericht mit den
   Nachtwerten (Median 03–05 Uhr).

## Raumzuordnung und Zielbereiche

Zuordnung von Eric bestätigt am 2026-11-22. Mit ¹ markierte Räume haben noch
kein Raumthermometer. Dort misst ein Rauchmelder an der Decke, der eher zu
viel anzeigt.

| Raum | Sensor | Ziel °C | Herkunft |
|---|---|---|---|
| Schlafzimmer | Schlafzimmer Temperatur | 17–18 | UBA: 17; Erics Wunsch |
| Büro/Gäste ¹ | Gästezimmer Rauchmelder | 20–21 | Erics Vorgabe „genutzt“ |
| Zimmer Weiß ¹ | Kinderzimmer Rauchmelder | 20–21 | Erics Vorgabe „genutzt“ |
| Kinderzimmer Velux | Baby Temperatur | 20–22 | eigene Schätzung |
| Flur OG ¹ | Obergeschoss Flur Rauchmelder | 20–21 | Erics Vorgabe 2026-11-25: grenzt an alle Räume, wie die übrigen genutzten Räume |
| Bad | Badezimmer Temperatur | 21–22 | gebräuchlicher Komfortwert |
| EG (Wohnen, Essen, WC, Küche, Eingang, Kaminzimmer ¹) | jeweiliger Raumsensor | 20–21 | Erics Vorgabe: EG einheitlich |
| Büro (EG) | Büro Temperatur | 20,5–21,5 | Vorgabe 21 °C; ±0,5 K eigene Wahl |
| UG (Hobby ¹, Waschküche ¹, Bar, Sauna ¹) | Hobbyraum/Waschraum/Sportraum Rauchmelder, Bar Temperatur | 17,5–18,5 | Vorgabe UG einheitlich 18 °C; ±0,5 K eigene Wahl |

Ohne Raumsensor und deshalb nicht bewertet: Vorrat, Diele UG und WC/Dusche
UG.

## Regeln der Auswertung

Kennzeichnung: **[Dok]** steht so in Erics Arbeitsdokument „Heizkreise und
Referenzraum“ vom 2026-11-22 (dort mit Quellen). **[eigen]** ist eine eigene
Festlegung ohne externe Quelle.

- **Ampel pro Raum:** Grün bedeutet, der Median liegt im Zielbereich. Gelb
  bedeutet bis 1 K daneben, Rot mehr als 1 K daneben. Die 1-K-Schwelle
  stammt aus der Referenzraum-Regel aus Phase 3 [Dok]. Die Farbabstufung
  ist [eigen].
- **Bewertungsgrundlage:** Median über 48 h bzw. Nachtwerte von 03–05 Uhr,
  nie Momentwerte [Dok]. Gemittelt wird über Messwerte, nicht über die Zeit
  [eigen; Vereinfachung].
- **Zielraum:** Er muss grün sein, damit der Schritt bestätigt wird [Dok].
  Gelb führt zu „beobachten“, rot zu „zurücknehmen“ [eigen]. Bei
  „Alle Räume“ zählt der schlechteste bewertete Raum.
- **Spreizung:** Sie darf sich nicht verschlechtern [Dok]. Das Ziel sind
  4–7 K [Dok]. Als Verschlechterung gilt, wenn der Abstand zum Zielband um
  mehr als 0,3 K wächst [eigen; die ebusd-Auflösung beträgt 0,5 K].
- **Verdichterstarts pro Tag:** Sie dürfen nicht steigen [Dok]. Als Anstieg
  gilt mehr als +1 Start pro Tag oder mehr als +10 %, je nachdem, was größer
  ist [eigen].
- **Laufzeit pro Start:** Unter 10 min gibt es einen Hinweis [Dok].
- **Schlafzimmer:** Unter 16 °C oder ab 60 % Luftfeuchte gilt der Schritt
  als fehlgeschlagen [Dok].
- **Außentemperatur:** Weicht das Mittel vorher und nachher um mehr als
  2 K ab, gibt es einen Hinweis „Vergleich unsicher“ [eigen].
- **Spanne EG/UG:** Max. minus min. der Raum-Mediane einer Etage, nur als
  Information. Zum Vergleich: Benachbarte Räume sollen höchstens ca. 2 K
  auseinanderliegen [Dok].

**Fazit:** Gibt es ein Problem, lautet es „zurücknehmen“. Gibt es nur
Hinweise, lautet es „beobachten“. Ist alles erfüllt, lautet es
„bestätigt“. Ohne gespeicherte Ausgangswerte steht dort „kein
Ausgangswert“.

## Bekannte Grenzen

- Verdichterstarts, Kompressorstunden und Energie werden als Änderung
  innerhalb des Fensters gemessen. Die erste Zählerstufe im Fenster kann
  dabei fehlen, sodass bis zu 1 Start bzw. 1 h zu wenig gezählt werden. Der
  Fehler tritt vorher und nachher gleich auf.
- Die Kompressorstunden haben 1 h Auflösung, die Laufzeit pro Start ist
  deshalb nur grob.
- Die Spreizung ist die Spreizung der Wärmepumpe hinter der Weiche MPS 40,
  nicht die der Heizkreise (siehe `docs/EBUSD_REGISTERS.md`).
- Energie, normiert auf Heizgradtage über 2–3 Wochen [Dok], rechnet die
  Automation nicht. Das bleibt eine manuelle Auswertung.
