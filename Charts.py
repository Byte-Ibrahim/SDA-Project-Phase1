import csv
import matplotlib.pyplot as plt
import seaborn as sns
from functools import reduce

def load_gdp_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_reader = list(csv.DictReader(f))
            if not raw_reader: return []
            
            year_cols = list(filter(lambda c: c.isdigit(), raw_reader[0].keys()))
            
            no_global = filter(lambda r: r.get("Continent", "").strip().lower() != "global", raw_reader)
            
            # Map each row to year-specific records
            def row_mapper(row):
                cont = row.get("Continent", "Unknown").strip()
                name = row.get("Country Name", "Unknown").strip()
                return map(lambda yr: {
                    "country": name,
                    "continent": cont,
                    "year": int(yr),
                    "gdp": float(row[yr]) if row.get(yr) not in [None, ""] else None
                }, year_cols)

            mapped_data = map(row_mapper, no_global)
            
            # remove None GDPs
            def flattener(acc, current_map_obj):
                acc.extend(filter(lambda x: x is not None, current_map_obj))
                return acc
            
            return reduce(flattener, mapped_data, [])
            
    except Exception as e:
        print(f"Processing Error: {e}")
        return []

def generate_charts(data):
    
    valid_data = list(filter(lambda x: x.get("gdp") is not None, data))
    if not valid_data:
        print("No valid GDP data to generate charts.")
        return

    region_totals = reduce(
        lambda acc, x: {**acc, x['continent']: acc.get(x['continent'], 0) + x['gdp']},
        valid_data, {}
    )
    
    conts, vals = list(region_totals.keys()), list(region_totals.values())

    # --- CHART 1: Pie Chart ---
    plt.figure(figsize=(8, 6))
    plt.pie(vals, labels=conts, autopct='%1.1f%%')
    plt.title("GDP Share by Continent (Functional)")
    plt.savefig('gdp_pie.png')
    plt.close()

    # --- CHART 2: Bar Chart ---
    plt.figure(figsize=(10, 5))
    sns.barplot(x=conts, y=vals, palette="viridis")
    plt.title("Total Cumulative GDP by Region")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('gdp_bar.png')
    plt.close()

    latest_yr = max(map(lambda x: x['year'], valid_data))
    yr_data = sorted(
        filter(lambda x: x['year'] == latest_yr and x['gdp'] is not None, valid_data),
        key=lambda x: x['gdp'], reverse=True
    )[:10]
    
    if not yr_data:
        print(f"No GDP data for year {latest_yr}")
        return

    c_names = list(map(lambda x: x['country'], yr_data))
    c_gdps = list(map(lambda x: x['gdp'], yr_data))

    # --- CHART 3: Line Plot ---
    plt.figure(figsize=(10, 5))
    plt.plot(c_names, c_gdps, marker='o', color='blue', linestyle='--')
    plt.title(f"Top 10 Countries GDP in {latest_yr} (Line)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('gdp_line.png')
    plt.close()

    # --- CHART 4: Scatter Plot ---
    plt.figure(figsize=(10, 5))
    sns.scatterplot(x=c_names, y=c_gdps, hue=c_names, s=150, legend=False)
    plt.title(f"GDP Distribution Top 10 ({latest_yr})")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('gdp_scatter.png')
    plt.close()

if __name__ == "__main__":
    gdp_list = load_gdp_data('gdp.csv')
    if gdp_list:
        generate_charts(gdp_list)
        print("Success: Charts created using map, filter, and reduce!")
    else:
        print("Error: Could not load data. Check if gdp.csv is in the folder.")
