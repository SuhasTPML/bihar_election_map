#!/usr/bin/env python3
"""Convert JSON array files back to CSV.

Usage: python json_to_csv.py parties.json bihar_election_results_consolidated.json
Outputs use .csv extension in same directory.
"""

import csv
import json
import pathlib
import sys
from typing import Any, List


def json_to_records(json_path: pathlib.Path) -> List[dict[str, Any]]:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"Expected list at top level in {json_path.name}")
    return data


def write_csv(records: List[dict[str, Any]], csv_path: pathlib.Path) -> None:
    if not records:
        csv_path.write_text("", encoding="utf-8")
        return

    fieldnames = list(records[0].keys())
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def convert_file(json_path: pathlib.Path) -> None:
    records = json_to_records(json_path)
    csv_path = json_path.with_suffix(".csv")
    write_csv(records, csv_path)
    print(f"Converted {json_path.name} -> {csv_path.name} ({len(records)} records)")


def main(args: List[str]) -> None:
    if not args:
        print("Usage: python json_to_csv.py <file1.json> [file2.json ...]")
        sys.exit(1)

    for arg in args:
        path = pathlib.Path(arg)
        if not path.exists():
            print(f"Skipping {arg}: file not found")
            continue
        convert_file(path)


if __name__ == "__main__":
    main(sys.argv[1:])
