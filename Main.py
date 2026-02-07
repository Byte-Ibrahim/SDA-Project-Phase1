from Demo import load_gdp_data 
from Filter import filter_gdp_data,load_config
from Manipulation import Sum_gdp_region

def main():
    # Load GDP data
    data = load_gdp_data("gdp.csv")
    print("Total records loaded:", len(data))
    #print("Sample record:", data[0])

    # Load config
    config = load_config("config.json")
    print("\nFiltering with config:", config)

    # Filter data
    filtered_data,operation = filter_gdp_data(data, config)
    print("Total records after filter:", len(filtered_data))
    #print("Sample filtered record:", filtered_data[0] if filtered_data else "No records match")

    # Calculate GDP Sum for Region
    total = Sum_gdp_region(filtered_data,config,operation)
    print(total)




if __name__ == "__main__":
    main()