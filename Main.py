from Demo import load_gdp_data 
from Filter import filter_gdp_data,load_config

def main():
    # Load GDP data
    data = load_gdp_data("gdp.csv")
    print("Total records loaded:", len(data))
    print("Sample record:", data[0])

    # Load config
    config = load_config("config.json")
    print("\nFiltering with config:", config)

    # Filter data
    filtered_data = filter_gdp_data(data, config)
    print("Total records after filter:", len(filtered_data))
    print("Sample filtered record:", filtered_data[0] if filtered_data else "No records match")

if __name__ == "__main__":
    main()