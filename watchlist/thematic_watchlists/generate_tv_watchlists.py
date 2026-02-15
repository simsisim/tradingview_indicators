import pandas as pd
import os

def generate_watchlist(csv_path, output_name, cluster_id_col, cluster_name_col):
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return set()

    df = pd.read_csv(csv_path)
    
    # Check for duplicates
    duplicates = df[df.duplicated(subset=['Symbol'], keep=False)]
    if not duplicates.empty:
        print(f"\n[!ALERT] Duplicates found in {csv_path}:")
        # Determine info column (Description for industries, Country for countries)
        info_col = 'Description' if 'Description' in df.columns else 'Country'
        cols_to_show = ['Symbol', info_col] if info_col in df.columns else ['Symbol']
        print(duplicates[cols_to_show].sort_values('Symbol'))
        # Remove duplicates for the watchlist but keep the first occurrence
        df = df.drop_duplicates(subset=['Symbol'], keep='first')

    # Sort by Cluster ID
    df = df.sort_values(by=cluster_id_col)

    with open(output_name, 'w') as f:
        current_cluster = None
        for _, row in df.iterrows():
            cluster_name = row[cluster_name_col]
            if cluster_name != current_cluster:
                f.write(f"### {cluster_name}\n")
                current_cluster = cluster_name
            f.write(f"{row['Symbol']}\n")

    print(f"Watchlist saved to {output_name}")
    return set(df['Symbol'])

if __name__ == "__main__":
    # Define paths based on current directory listing
    # We use the names found in the latest list_dir: ETFs-industries-clustered.csv and ETFs-countries-clustered.csv
    industry_csv = "ETFs-industries-clustered.csv"
    country_csv = "ETFs-countries-clustered.csv"
    
    industry_out = "io-ETFs-industries.txt"
    country_out = "io-ETFs-countries.txt"

    print("--- Generating Industry Watchlist ---")
    ind_symbols = generate_watchlist(industry_csv, industry_out, "Cluster_ID", "Cluster_Name")

    print("\n--- Generating Country Watchlist ---")
    count_symbols = generate_watchlist(country_csv, country_out, "Region_Code", "Region")

    # Cross-file duplicate check
    cross_dupes = ind_symbols.intersection(count_symbols)
    if cross_dupes:
        print(f"\n[!ALERT] Cross-file duplicates found (Symbol in both Industry and Country lists):")
        print(sorted(list(cross_dupes)))
