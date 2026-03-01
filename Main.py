from Loader import load_gdp_data,load_config
from Filter import filter_gdp_data
from Manipulation import Statistical_Analysis
from DashBoard import DashBoard

def main():
    # Load GDP data
    data = load_gdp_data("gdp.csv")

    # Load config
    config = load_config("config.json")

    # Filter data
    filtered_data = filter_gdp_data(data, config)

    operation=config.get('operation')
    # Calculate Statistical Analysis for given config file
    total = Statistical_Analysis(filtered_data,config,operation,data)
        
    # Displaying all the results and Analysis
    DashBoard(data,config,total)

   


if __name__ == "__main__":
    main()