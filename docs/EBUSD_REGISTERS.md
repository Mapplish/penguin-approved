# eBUS / Vaillant Register Reference

Domain knowledge about the ebusd registers exposed for this system's Vaillant
heat pump (aroTHERM-class, sensoCOMFORT VRC 720 controller, doc-ref
0020334315_06), collected while building dashboards and COP tracking. Keep
this updated whenever a new register or enum gets identified — the goal is
to stop re-deriving the same facts from scratch every session.

Live values can be pulled from the running instance via the Supervisor
proxy over SSH (see CLAUDE.md for the `penguin-pi` SSH quirks):

```
ssh penguin-pi "bash -lc 'curl -s -H \"Authorization: Bearer \$SUPERVISOR_TOKEN\" http://supervisor/core/api/states/<entity_id>'"
```

This works for entities that are **not** exposed on the "Freigegebene
Entitäten" page too (unlike the MCP `GetLiveContext` tool, which only sees
exposed entities) — most of the `hmu`/`ctlv2` power, mode and status
entities used for COP tracking are not exposed, so this is the only way to
inspect them live.

## Key enums

### `sensor.heating_ebusd_hmu_rundatastatuscode`

The most useful single field for figuring out *what the compressor is
currently doing*. Real-time status code from the HMU (Heizungsmanagement-
Unit) run data. Relevant values (there are ~50 total, mostly fault codes —
see the entity's `options` attribute for the full list):

| Value | Meaning |
|---|---|
| `standby` | Idle, nothing running |
| `heat_prerun` / `heat_compressor_active` / `heat_overrun` | Heating cycle: pre-run, compressor actively heating, overrun |
| `hwc_prerun` / `hwc_compressor_active` / `hwc_overrun` | Hot water (Warmwasser) cycle |
| `cool_prerun` / `cool_compressor_active` / `cool_overrun` | Cooling cycle |
| `heat_immersion_heater_active` / `hwc_immersion_heater_active` | Backup electric resistive heater running (not the compressor) — excluded from heat-pump COP calculations on purpose, since its efficiency is trivially ~1 and would corrupt the metric |
| `deicing_active` | Defrost cycle |

Used in `configuration.yaml` to gate the per-mode power sensors
(`sensor.waermepumpe_strom_*` / `sensor.waermepumpe_ertrag_*`) so energy can
be attributed to Heizen/Warmwasser/Kühlen instead of lumped together. Only
the `*_compressor_active` states are treated as "producing" — prerun/overrun
phases are pump-only and would dilute the COP.

### `sensor.heating_ebusd_hmu_setmode_hcmode`

Options: `auto`, `off`, `heat`, `water`. This is the **commanded** mode sent
to the HMU, not the live operating state — use `rundatastatuscode` for "what
is it doing right now".

### `sensor.heating_ebusd_hmu_status_hcmode`

Options: `off`, `cooling`, `heat`, `water`. Was `unknown` as of 2026-08-18
(never observed live). Might be a cleaner "current mode" signal than
`rundatastatuscode` if it turns out to be populated during actual cooling —
worth re-checking once the system has run through a cooling cycle.

### `sensor.heating_ebusd_ctlv2_hwcopmode` / `z1opmode` / `z2opmode` / `z3opmode`

Options: `off`, `auto`, `day`, `night`. Per-zone/hot-water operating mode as
set in the controller UI (Heizkreis/Warmwasser Betriebsart).

### `sensor.heating_ebusd_ctlv2_z1sfmode` / `z2sfmode` / `z3sfmode` / `hwcsfmode`

Options: `auto`, `ventilation`, `party`, `veto`, `onedayaway`,
`onedayathome`, `load`. "Sonderfunktion" special-function mode. Strongly
suspected mapping to the manual's Party/Lüften/1 Tag weg/1 Tag daheim/Laden
menu items, but not yet confirmed against the physical sensoCOMFORT display.

## Open verification items (unconfirmed against the physical display)

These dashboard labels are marked "(ungeprüft)" in
`homeassistant/dashboards/waermepumpe.yaml` because no exact wording match
was found in the manual/Fachhandwerker documentation. Live values as of
2026-08-17:

| Entity | Dashboard label | Live value | What to check on-device |
|---|---|---|---|
| `sensor.heating_ebusd_ctlv2_z1sfmode` / `hwcsfmode` | Sonderfunktion-Modus | `auto` (both) | Menü → Heizkreis 1 / Warmwasser → Sonderfunktionen |
| `sensor.heating_ebusd_ctlv2_z1quickvetotemp` | Kurzzeit-Veto-Temperatur | 21°C | Does the Party special function propose/show 21°C? |
| `sensor.heating_ebusd_ctlv2_z1holidaytemp` | Urlaubstemperatur | 15°C | Menü → Heizkreis 1 → Abwesenheit/Urlaub |
| `sensor.heating_ebusd_ctlv2_hc1excesstemp` | Überschusstemperatur | 0.0 K | No menu item found in either manual — likely stays unverified |
| `sensor.heating_ebusd_ctlv2_hc1heatcurveadaption` | Heizkurve-Adaption | 0.0 | Likely an internal diagnostic value, not a menu item (consistent with `AdaptHeatCurve: no`) |

Also confirmed: the additional Fachhandwerker-level parameters in the manual
(Bivalenzpunkt, Legionellenschutz-Zeit/Tag, Speicherladung Hysterese/Offset,
Systemschema-Code, Kreisart) do **not** exist as HA entities on this
installation — the ebusd config doesn't expose those registers. Adding them
would require extending the ebusd configuration itself.

**Kühlen/cooling COP is unverified end-to-end**: it's unknown whether
`sensor.heating_ebusd_hmu_currentyieldpower` reports meaningful values during
a cooling cycle (vs. only being populated for heating). Can only be checked
once the system actually runs `cool_compressor_active` — worth revisiting
once cooling season data exists.

## HA YAML gotcha: entity_id ≠ slugify(name) the way you'd expect

Not eBUS-specific, but discovered while wiring this up and worth keeping
here since it directly affects how new registers should be named. Home
Assistant's `slugify()` strips diacritics via Unicode NFKD decomposition +
ascii-ignore encoding — it does **not** transliterate German umlauts
(ä→ae, ü→ue, ö→oe) the way a human would. `"Wärmepumpe"` becomes
`"warmepumpe"`, `"Kühlen"` becomes `"kuhlen"`. Since entity_id is derived
from `name:` at first creation (not from `unique_id:`), any sensor whose
`name:` contains an umlaut will get a less-obvious entity_id than expected —
and once registered, that entity_id is sticky; renaming `name:` later does
**not** change it, only `unique_id:` forces re-registration under a new id.

Rule of thumb for this repo: give internally-referenced sensors (ones read
by *other* sensors' Jinja, or targeted by dashboards) ASCII-only `name:`
values (e.g. "Waermepumpe", "Kuehlen"), and keep the pretty German spelling
in dashboard-level `name:` overrides instead, where it's just a display
string with no entity_id consequences. Always run
`python scripts/check_config.py` before deploying — it catches exactly this
class of mismatch.
