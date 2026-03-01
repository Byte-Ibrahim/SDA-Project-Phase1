"""
plugins/inputs.py
-----------------
Input plugins: CSVReader, JSONReader.

Each calls service.execute(raw_data) to hand data to the Core.
They do NOT import anything from core/ except the PipelineService Protocol
(which is only used for type-hinting — no hard coupling).

Satisfies the PipelineService contract via duck typing.
"""

import csv
import json
from functools import reduce
from typing import Any, List


class CSVReader:

    def __init__(self, service, file_path: str):
        
        self.service   = service
        self.file_path = file_path

    def run(self) -> None:
        raw_data = self.load()
        self.service.execute(raw_data)

    def load(self) -> List[dict]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                year_cols = list(filter(lambda col: col.strip().isdigit(), reader.fieldnames))

                rows = list(map(
                    lambda row: list(map(
                        lambda year: {
                            "country":   row.get("Country Name", "").strip(),
                            "continent": row.get("Continent", "").strip(),
                            "year":      int(year),
                            "gdp":       float(row[year]) if row[year].strip() else None
                        },
                        year_cols
                    )),
                    reader
                ))

            return reduce(lambda a, b: a + b, rows, [])

        except FileNotFoundError:
            raise Exception(f"[CSVReader] File not found: {self.file_path}")


class JSONReader:

    def __init__(self, service, file_path: str):
        self.service   = service
        self.file_path = file_path

    def run(self) -> None:
        raw_data = self.load()
        self.service.execute(raw_data)

    def load(self) -> List[dict]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            return list(map(
                lambda r: {
                    "country":   str(r.get("country", "")).strip(),
                    "continent": str(r.get("continent", "")).strip(),
                    "year":      int(r.get("year", 0)),
                    "gdp":       float(r["gdp"]) if r.get("gdp") is not None else None
                },
                data
            ))

        except FileNotFoundError:
            raise Exception(f"[JSONReader] File not found: {self.file_path}")
        except json.JSONDecodeError:
            raise Exception(f"[JSONReader] Invalid JSON in: {self.file_path}")
