import csv
import json
from functools import reduce

def load_gdp_data(file_path):

    """
    Loads a wide-format GDP CSV and converts it into a list of dictionaries:
    Each dict has: country, continent, year, gdp
    """

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # Find all year columns (digits only)
            year_columns = list(filter(lambda col: col.isdigit(), reader.fieldnames))

            # Transform each row into multiple year-dict entries


            data = list(
                map(
                    lambda row: list(
                        map(
                            lambda year: {
                                "country": row.get("Country Name", "").strip(),
                                "continent": row.get("Continent", "").strip(),
                                "year": int(year),
                                "gdp": float(row[year]) if row[year].strip() else None
                            },
                            year_columns
                        )
                    ),
                    reader
                )
            )

            # Flatten the list of lists
            return reduce(lambda a, b: a + b, data, [])

    except FileNotFoundError:
        raise Exception("CSV file not found. Please check the path.")


# ---------- Load Config ----------
def load_config(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise Exception("Config file not found. Please check the path.")
    except json.JSONDecodeError:
        raise Exception("Config file is not a valid JSON.")
