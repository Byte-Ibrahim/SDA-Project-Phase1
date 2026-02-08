from Visualization import Graph_Visualizations


def DashBoard(data,config,Statistics):
    print("*===== DASHBOARD CONFIG =====*")
    print("\nFiltering with config: ", config)
    
    print("\n+++Statistical Analysis +++\n")

    if config.get("operation") != "Average_c":
        print(f"After applying {config.get('operation')} operation on the GDP of {config.get('continent')}, the result is ${Statistics:,.2f}\n")
    else:
        print(f"After applying {config.get('operation')} operation on the GDP of {config.get('country')} in {config.get('continent')} , the result is ${Statistics:,.2f}\n")

    # Displaying graphs, Region wise Analysis and Year wise Analysis
    print("\n+++ Visualizations +++\n")
    print("Loading Region wise and Year wise Graph Analysis Over GDP for given Dataset....\n")
    Graph_Visualizations(data)