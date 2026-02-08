
from functools import reduce

def Statistical_Analysis(filtered_data,config,operation):
    if operation=='Sum_r':
        return Sum_gdp_region(filtered_data,config)
    elif operation=='Average_r':
        return Avg_gdp_region(filtered_data,config)
    elif operation=='Average_c':
        return Avg_gdp_region(filtered_data,config)

    


def Sum_gdp_region(filtered_data,config):

    # Deriving Continents from Config.json
    continents = list(map(lambda x: x.strip(), config.get("continent").split("&")))

    # Filtering GDP for the given Continent
    filtered_sum_region = filter(
            lambda row:row['continent'] in continents and 
            row['gdp'] is not None,
            filtered_data
            )
    
    # Separating GDP values
    gdp_values = list(map(lambda row:row['gdp'],filtered_sum_region))
    
    # Summation of GDP values
    return reduce(lambda a,b:a+b,gdp_values,0)

def Avg_gdp_region(filtered_data,config):
    return Sum_gdp_region(filtered_data,config)/float(len(filtered_data))

def Avg_gdp_Country(filtered_data,config):

    # Deriving Country from Config.json
    country = list(map(lambda x: x.strip(), config.get("country").split("&")))
    
    # Filtering GDP for the given Country
    filtered_sum_region = filter(
            lambda row:row['country'] in country and 
            row['gdp'] is not None,
            filtered_data
            )
    
    # Separating GDP values
    gdp_values = list(map(lambda row:row['gdp'],filtered_sum_region))
    
    # Summation of GDP values
    sum = reduce(lambda a,b:a+b,gdp_values,0)

    # Returning AVG
    return sum/float(len(filtered_data))