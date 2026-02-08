from Loader import load_gdp_data 
from Filter import filter_gdp_data,load_config
from Manipulation import Statistical_Analysis
from DashBoard import DashBoard

def main():
    # Load GDP data
    data = load_gdp_data("gdp.csv")

    # Load config
    config = load_config("config.json")

    # Filter data
    filtered_data,operation = filter_gdp_data(data, config)

    # Calculate Statistical Analysis for given config file
    total = Statistical_Analysis(filtered_data,config,operation)
        
    # Displaying all the results and Analysis
    DashBoard(data,config,total)

   


if __name__ == "__main__":
    main()