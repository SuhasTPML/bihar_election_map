#!/usr/bin/env python3
"""Convert CSV files to JSON with schema-aware tweaks.

Usage: python csv_to_json.py parties.csv bihar_election_results_consolidated.csv
Outputs sit alongside inputs with .json extension.

Schema notes:
- parties.csv -> parties.json (new format)
  Input columns may include alliance_2020, alliance_2015, alliance_2010.
  Output uses a single field `alliance` derived from `alliance_2020` (or
  falls back to an existing `alliance` column if present). Historical
  alliance columns are dropped in the JSON output.
- Other CSV files are converted as-is (row-per-object) without field
  renaming.
"""

import csv
import json
import pathlib
import sys
from typing import Any, List, Dict


def csv_to_records(csv_path: pathlib.Path) -> List[Dict[str, Any]]:
    with csv_path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def write_json(records: List[Dict[str, Any]], json_path: pathlib.Path) -> None:
    json_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")


def convert_file(csv_path: pathlib.Path) -> None:
    records = csv_to_records(csv_path)

    # Schema-aware transformation for parties.csv -> new parties.json
    if csv_path.stem.lower().startswith("parties") and records:
        transformed: List[Dict[str, Any]] = []
        for row in records:
            # Prefer explicit 2020/current alliance if available; else fallback
            alliance = (
                row.get("alliance_2020")
                or row.get("alliance")
                or ""
            )
            transformed.append(
                {
                    "code": row.get("code", "").strip(),
                    "name": row.get("name", "").strip(),
                    "alliance": alliance.strip(),
                    "color": row.get("color", "").strip(),
                }
            )
        records = transformed

    json_path = csv_path.with_suffix(".json")
    write_json(records, json_path)
    print(f"Converted {csv_path.name} -> {json_path.name} ({len(records)} records)")


def main(args: List[str]) -> None:
    if not args:
        print("Usage: python csv_to_json.py <file1.csv> [file2.csv ...]")
        sys.exit(1)

    for arg in args:
        path = pathlib.Path(arg)
        if not path.exists():
            print(f"Skipping {arg}: file not found")
            continue
        convert_file(path)


if __name__ == "__main__":
    main(sys.argv[1:])
