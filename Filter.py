# ---------- Filter Function ----------
import json

# ---------- Config Validation ----------
def validate_config(data,config):
    # 1. Check required fields
    required_fields = ["continent", "year", "operation", "output"]
    missing = [f for f in required_fields if f not in config]
    if missing:
        raise ValueError(f"Missing config fields: {missing}")

    # 2. Type checks
    if not isinstance(config["continent"], str):
        raise TypeError("continent must be a string")
    if not isinstance(config["year"], int):
        raise TypeError("year must be an integer")
    if config["operation"] not in ["Sum", "Average"]:
        raise ValueError("operation must be 'Sum' or 'Average'")
    if not isinstance(config["output"], str):
        raise TypeError("output must be a string")

    # 3. Check if continent exists in dataset
    available_continents = set(r["continent"] for r in data)
    continents = [c.strip() for c in config["continent"].split("&")]
    invalid_continents = [c for c in continents if c not in available_continents]
    if invalid_continents:
        raise ValueError(f"Invalid continent(s) in config: {invalid_continents}")

    # 4. Check if year exists in dataset
    available_years = set(r["year"] for r in data)
    if config["year"] not in available_years:
        raise ValueError(f"Year {config['year']} not found in dataset")


# ---------- Filter Function ----------
def filter_gdp_data(data, config):
    # Validate config before filtering
    validate_config(data, config)

    continents = list(r.strip() for r in config.get("continent", "").split("&")) 

    year_filter = config.get("year") 
    operation=config.get("operation")

    # Filter rows where continent matches AND year matches
    filtered = list(
        filter(
            lambda row: row['continent'] in continents and
            row['year'] == year_filter,
            data
        )
    )
    
    return filtered, operation


# ---------- Load Config ----------
def load_config(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise Exception("Config file not found. Please check the path.")
    except json.JSONDecodeError:
        raise Exception("Config file is not a valid JSON.")
