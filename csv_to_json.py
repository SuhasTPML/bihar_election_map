#!/usr/bin/env python3
"""Convert CSV files to JSON copies.

Usage: python csv_to_json.py parties.csv bihar_election_results_consolidated.csv
Outputs sit alongside inputs with .json extension.
"""

import csv
import json
import pathlib
import sys
from typing import Any, List


def csv_to_records(csv_path: pathlib.Path) -> List[dict[str, Any]]:
    with csv_path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def write_json(records: List[dict[str, Any]], json_path: pathlib.Path) -> None:
    json_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")


def convert_file(csv_path: pathlib.Path) -> None:
    records = csv_to_records(csv_path)
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
