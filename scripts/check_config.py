#!/usr/bin/env python3
"""Validate configuration.yaml and homeassistant/**/*.yaml before deploying.

Run this before every deploy to the Pi (see CLAUDE.md). Catches the two bug
classes that have actually broken this config in the past:

1. YAML syntax errors.
2. Self-referential entity_id mismatches: this repo defines a bunch of
   template/integration/utility_meter sensors and then references them by
   entity_id elsewhere (in other sensors' Jinja, or in dashboards). The
   entity_id HA assigns is slugify(name) -- and HA's slugify() strips
   diacritics (Unicode NFKD + ascii-ignore) rather than transliterating them
   (ä -> a, not ae; ü -> u, not ue). A name like "Wärmepumpe" becomes
   "warmepumpe", not "waermepumpe". Getting this wrong silently creates a
   *different* entity than the one every reference expects -- HA itself
   won't complain, the entity registry just quietly diverges. This script
   recomputes the real entity_id for every sensor we define and cross-checks
   it against every reference in the repo.
3. Duplicate unique_id values, which cause HA to only register one of the
   colliding entities.

This only validates entities *this repo defines*. References to entities
that come from live integrations (ebusd, HACS components, etc.) can't be
checked statically -- verify those against the running instance instead,
e.g. via the Supervisor REST API (see docs/EBUSD_REGISTERS.md).
"""

import re
import sys
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_YAML = REPO_ROOT / "configuration.yaml"
HA_DIR = REPO_ROOT / "homeassistant"

# Prefixes for entity_ids this repo generates itself. Only references
# starting with one of these are checked against the defined set -- anything
# else is assumed to come from a live integration and is left alone.
INTERNAL_PREFIXES = (
    "waermepumpe_",
    "heat_pump_cop",
    "compressor_runtime_per_start",
    "next_cover_automation",
)


def ha_slugify(name: str) -> str:
    """Reimplementation of Home Assistant's util.slugify() for our purposes.

    HA decomposes unicode (NFKD) and drops anything that doesn't survive an
    ascii encode -- so combining diacritics (umlaut dots, accents) are
    dropped, not transliterated. Verified empirically against a live HA
    2026.8 instance: "Wärmepumpe" -> "warmepumpe", "Kühlen" -> "kuhlen".
    """
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    name = name.strip("_")
    name = re.sub(r"_+", "_", name)
    return name


HA_YAML_TAGS = ("!include_dir_merge_named", "!include_dir_named", "!include", "!secret")


def strip_ha_tags(text: str) -> str:
    """Neutralize HA's custom YAML tags (!include, !secret, ...) so PyYAML
    can parse the file structurally. We don't need the resolved values.

    Only strips the specific tag names this repo uses, anchored to tag
    position (start of value, i.e. preceded by whitespace) -- NOT any
    bare '!' anywhere, since '!' shows up inside plain string values too
    (e.g. notification titles like "Wasserleck erkannt!")."""
    pattern = r"(?<=\s)(" + "|".join(re.escape(t) for t in HA_YAML_TAGS) + r")\S*"
    return re.sub(pattern, "", text)


def load_yaml_safely(path: Path):
    import yaml

    text = path.read_text(encoding="utf-8")
    text = strip_ha_tags(text)
    try:
        return yaml.safe_load(text), None
    except yaml.YAMLError as exc:
        return None, str(exc)


def extract_defined_sensors(config_text: str):
    """Find every `name: "..."` and `unique_id: ...` pair inside
    template/integration/utility_meter sensor blocks and derive the
    resulting entity_id. Returns (defined_entity_ids, unique_id_list)."""
    defined = set()
    unique_ids = []

    # name: "..." possibly followed a few lines later by unique_id: ...
    # We pair them up positionally: for each `name:` line, look at the
    # nearest `unique_id:` within the next few lines (mirrors how every
    # block in this file is written).
    lines = config_text.splitlines()
    name_pattern = re.compile(r'^\s*-?\s*name:\s*"([^"]+)"\s*$')
    uid_pattern = re.compile(r"^\s*unique_id:\s*(\S+)\s*$")

    for i, line in enumerate(lines):
        m = name_pattern.match(line)
        if not m:
            continue
        name = m.group(1)
        entity_id = "sensor." + ha_slugify(name)
        defined.add(entity_id)
        for j in range(i + 1, min(i + 4, len(lines))):
            um = uid_pattern.match(lines[j])
            if um:
                unique_ids.append((um.group(1), entity_id, i + 1))
                break

    return defined, unique_ids


def extract_entity_references(text: str):
    return set(re.findall(r"\bsensor\.[a-z0-9_]+\b", text))


def check_lovelace_dashboard_urls(config: dict):
    """HA requires every lovelace dashboard's url_path (the YAML key under
    lovelace->dashboards) to contain a hyphen. Missing this doesn't just
    break that one dashboard -- it fails the whole 'lovelace' integration,
    which cascades into 'frontend', 'hacs', 'logbook', 'panel_custom' and
    everything else that depends on them. Caught the hard way once
    already; never again."""
    problems = []
    dashboards = (config or {}).get("lovelace", {}).get("dashboards", {}) or {}
    for url_path in dashboards:
        if "-" not in str(url_path):
            problems.append(
                f"lovelace dashboard url_path '{url_path}' has no hyphen -- "
                f"HA will refuse to set up the ENTIRE lovelace integration "
                f"(and everything depending on frontend/hacs/logbook with it). "
                f"Rename the key to include a '-', e.g. '{url_path}-x'."
            )
    return problems


def main() -> int:
    problems = []

    yaml_files = [CONFIG_YAML] + sorted(HA_DIR.rglob("*.yaml"))
    yaml_files = [p for p in yaml_files if p.exists()]

    parsed_config = None
    for path in yaml_files:
        parsed, err = load_yaml_safely(path)
        if err:
            problems.append(f"YAML syntax error in {path.relative_to(REPO_ROOT)}:\n  {err}")
        elif path == CONFIG_YAML:
            parsed_config = parsed

    if problems:
        # Don't bother with semantic checks if a file doesn't even parse.
        for p in problems:
            print("FAIL:", p)
        return 1

    problems.extend(check_lovelace_dashboard_urls(parsed_config))

    config_text = CONFIG_YAML.read_text(encoding="utf-8")
    defined, unique_ids = extract_defined_sensors(config_text)

    seen = {}
    for uid, entity_id, line_no in unique_ids:
        if uid in seen:
            problems.append(
                f"Duplicate unique_id '{uid}' at configuration.yaml:{line_no} "
                f"(first seen for {seen[uid]})"
            )
        else:
            seen[uid] = entity_id

    all_refs = set()
    for path in yaml_files:
        all_refs |= extract_entity_references(path.read_text(encoding="utf-8"))

    for ref in sorted(all_refs):
        obj_id = ref.split(".", 1)[1]
        if not obj_id.startswith(INTERNAL_PREFIXES):
            continue
        if ref not in defined:
            problems.append(
                f"Reference to '{ref}' looks internal but no sensor definition "
                f"produces that entity_id. Defined internal sensors: "
                f"{sorted(e for e in defined if e.split('.', 1)[1].startswith(INTERNAL_PREFIXES))}"
            )

    if problems:
        print(f"FAIL: {len(problems)} issue(s) found\n")
        for p in problems:
            print("-", p, "\n")
        return 1

    print(f"OK: {len(yaml_files)} YAML files valid, {len(defined)} internal sensors consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
