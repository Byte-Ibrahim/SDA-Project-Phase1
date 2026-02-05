import csv

def load_gdp_data(file_path):
    """
    Loads a wide-format GDP CSV and converts it into a list of dictionaries:
    Each dict has: country, continent, year, gdp
    """
    data = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
           
            # Find all columns that are years (numbers)
            year_columns = [col for col in reader.fieldnames if col.isdigit()]

            for row in reader:
                country = row.get("Country Name", "").strip()
                continent = row.get("Continent", "").strip()

                # Loop over all years and create one row per year
                for year in year_columns:
                    value = row.get(year, "").strip()
                    data.append({
                        "country": country,
                        "continent": continent,
                        "year": int(year),
                        "gdp": float(value) if value else None
                    })

        return data

    except FileNotFoundError:
        raise Exception("CSV file not found. Please check the path.")

