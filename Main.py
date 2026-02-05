from Demo import load_gdp_data

def main():
    data = load_gdp_data("gdp.csv")

    print("Total records loaded:", len(data))
    print("Sample record:", data[0])

if __name__ == "__main__":
    main()
