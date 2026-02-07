from Demo import load_gdp_data
from Filter import filter_gdp_data, load_config
from Manipulation import Sum_gdp_region
from Charts import generate_charts

def main():
    # ---------- Load GDP Data ----------
    data = load_gdp_data("gdp.csv")
    if not data:
        print("Error: No GDP data loaded. Check your file path or content.")
        return
    print("Total records loaded:", len(data))
    # print("Sample record:", data[0])

    # ---------- Load Config ----------
    config = load_config("config.json")
    print("\nFiltering with config:", config)

    # ---------- Filter Data ----------
    try:
        filtered_data, operation = filter_gdp_data(data, config)
    except Exception as e:
        print(f"Error during filtering: {e}")
        return

    print("Total records after filter:", len(filtered_data))
    # print("Sample filtered record:", filtered_data[0] if filtered_data else "No records match")

    if not filtered_data:
        print("No records match the filter. Exiting.")
        return

    # ---------- Calculate GDP Sum for Region ----------
    total = Sum_gdp_region(filtered_data, config, operation)
    print("\nRegion-wise GDP Summary:")
    for region, gdp_val in total.items():
        print(f"{region}: {gdp_val}")

    # ---------- Generate Charts ----------
    try:
        print("\nGenerating charts...")
        generate_charts(filtered_data)
        print("Charts created successfully! Check your project folder for PNG files.")
    except Exception as e:
        print(f"Error generating charts: {e}")


if __name__ == "__main__":
    main()
