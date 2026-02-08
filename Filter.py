# ---------- Filter Function ----------
import json

# ---------- Config Validation ----------
def validate_config(data,config):
    # 1. Check required fields
    required_fields = ["continent", "year", "operation", "output"]
    operation = config.get("operation")

    if operation=='Average_c':
        required_fields = ["continent","country", "year", "operation", "output"]

    missing = list(filter((lambda row:row not in config),required_fields))
    if missing:
        raise ValueError(f"Missing config fields: {missing}")

    # 2. Type checks
    if not isinstance(config["continent"], str):
        raise TypeError("continent must be a string")
    if  (operation=='Average_c') and (not isinstance(config["country"], str)):
        raise TypeError("country must be a string")
    if not isinstance(config["year"], int):
        raise TypeError("year must be an integer")
    if config["operation"] not in ["Sum_r", "Average_r","Average_c"]:
        raise ValueError("operation must be 'Sum_r' or 'Average_r' For Region/Continent and 'Average_c' For Country ")
    if not isinstance(config["output"], str):
        raise TypeError("output must be a string")

    # 3. Check if continent exists in dataset
    available_continents = set(r["continent"] for r in data)
    continents = list(map(lambda r : r.strip(),config['continent'].split("&")))

    invalid_continents = [c for c in continents if c not in available_continents]
    if invalid_continents:
        raise ValueError(f"Invalid continent(s) in config: {invalid_continents}")

    # 3. Check if country exists in dataset
    if operation =="Average_c":
        available_country = set(r["country"] for r in data)
        #country = list(map(lambda r : r.strip(),config['country'].split("&")))
        country = [config.get("country").strip()]
        invalid_country = [c for c in country if c not in available_country]
        if invalid_country:
            raise ValueError(f"Invalid country(s) in config: {invalid_country}")

    # 4. Check if year exists in dataset
    available_years = set(r['year'] for r in data)
    if config['year'] not in available_years:
        raise ValueError(f"Year {config['year']} not found in dataset")


# ---------- Filter Function ----------
def filter_gdp_data(data, config):

    # Validate config before filtering
    validate_config(data, config)

   # continents = list(map(lambda r : r.strip(),config['continent'].split("&")))
    continents=config.get("continent")
    
    if config.get('operation')=='Average_c':
        country = [config.get("country").strip()] 

    year_filter = config.get("year") 

    # Filter rows where continent matches AND year matches
    if config.get('operation')!='Average_c':
        filtered = list(
            filter(
                lambda row: row['continent'] in continents and
                #row['country'] in country and 
                row['year'] == year_filter,
                data
            )
        )
    else: # Filter rows where continent matches AND country AND year matches
        filtered = list(
            filter(
                lambda row: row['continent'] in continents and
                row['country'] in country and 
                row['year'] == year_filter,
                data
            )
        )

    return filtered


