from functools import reduce

def Sum_gdp_region(data, config=None, operation=None):
    """
    Takes a list of dictionaries with keys:
    country, continent, year, gdp

    Returns a dictionary:
    { continent: total_gdp }
    """
    # Filtering data which is not 0 or null
    filtered_data = list(filter(lambda row: row.get("gdp") is not None, data))

    # Using reduce func to accumulate sum
    def reducer(sumed, row):
        continent = row.get("continent")
        gdp = row.get("gdp")

        sumed[continent] = sumed.get(continent, 0) + gdp
        return sumed

    return reduce(reducer, filtered_data, {})
