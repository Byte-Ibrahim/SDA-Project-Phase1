
import json
def filter_gdp_data(data, config):
    """
    Filters GDP data according to the config dictionary.
    Uses `filter()` in functional style.
    """
    return list(
        filter(
            lambda row: (
                (row['continent'] == config.get('continent', row['continent'])) and
                (row['year'] >= config.get('year_min', row['year'])) and
                (row['year'] <= config.get('year_max', row['year'])) and
                (row['gdp'] is not None) and
                (row['gdp'] >= config.get('gdp_min', row['gdp'])) and
                (row['gdp'] <= config.get('gdp_max', row['gdp']))
            ),
            data
        )
    )

def load_config(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise Exception("Config file not found. Please check the path.")