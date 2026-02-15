import os

# Set environment variables to prevent non-fatal threadpoolctl warnings
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import pandas as pd
import numpy as np
import warnings
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# Suppress standard Python warnings
warnings.filterwarnings("ignore")

# Configuration
input_file = "/home/imagda/_invest2024/tradingview/watchlist/ETFs-countries.txt"
output_csv = "/home/imagda/_invest2024/tradingview/watchlist/ETFs-countries-clustered.csv"
output_plot = "/home/imagda/_invest2024/tradingview/watchlist/country_cluster_plot.html"

def get_region_mapping():
    """Returns a mapping from country name to region/continent."""
    return {
        "Thailand": "SE Asia",
        "South Korea": "East Asia",
        "Vietnam": "SE Asia",
        "Taiwan": "East Asia",
        "Australia": "Oceania",
        "Belgium": "Europe",
        "Canada": "North America",
        "Greece": "Europe",
        "Germany": "Europe",
        "Poland": "Europe",
        "Portugal": "Europe",
        "Spain": "Europe",
        "Italy": "Europe",
        "Brazil": "South America",
        "China": "East Asia",
        "Japan": "East Asia",
        "Turkey": "Middle East/Europe",
        "Israel": "Middle East",
        "Norway": "Europe",
        "Euro fins": "Europe",
        "Chin": "East Asia",  # Typo in source file
        "Hong Kong": "East Asia",
        "Saudi Arabia": "Middle East",
        "India": "South Asia",
        "Emerging Markets": "Global/Mixed"
    }

def perform_clustering():
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    # 1. Load Data
    # The file has some header-like rows but is effectively comma-separated
    df = pd.read_csv(input_file).drop_duplicates()
    df['Country'] = df['Country'].str.strip()
    print(f"Loaded {len(df)} country-based ETFs.")

    # 2. Map Regions
    region_map = get_region_mapping()
    df['Region'] = df['Country'].map(region_map).fillna("Unknown")

    # 3. Create simplified coordinates for visualization using Region
    # Since we don't have descriptions, we cluster primarily by Region
    # Factorize for K-means
    df['Region_Code'] = pd.factorize(df['Region'])[0]
    
    # We add some jitter to Dim1/Dim2 so plot looks better even with shared regions
    np.random.seed(42)
    df['Dim1'] = df['Region_Code'] + np.random.normal(0, 0.1, len(df))
    df['Dim2'] = np.random.normal(0, 0.5, len(df))

    # 4. Visualization
    fig = px.scatter(
        df, x='Dim1', y='Dim2',
        color='Region',
        text='Symbol',
        hover_data=['Country', 'Region'],
        title='ETF Countries: Geographic Clustering by Region',
        template='plotly_dark'
    )
    
    fig.update_traces(textposition='top center', marker=dict(size=12))
    fig.update_layout(
        showlegend=True,
        legend_title_text='Region',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=''),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title='')
    )

    # 5. Save results
    df.to_csv(output_csv, index=False)
    fig.write_html(output_plot)
    print(f"CSV saved to {output_csv}")
    print(f"Plot saved to {output_plot}")

if __name__ == "__main__":
    perform_clustering()
