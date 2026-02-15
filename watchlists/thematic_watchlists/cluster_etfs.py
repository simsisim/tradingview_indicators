import os

# Set these BEFORE any other imports to prevent threadpoolctl background discovery bugs
# in some Anaconda/Linux environments. This limits threading but keeps output clean.
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import pandas as pd
import numpy as np
import warnings

# Suppress standard Python warnings
warnings.filterwarnings("ignore")

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering
import plotly.express as px
import plotly.graph_objects as go
import os

# Configuration
input_file = "/home/imagda/_invest2024/tradingview/watchlist/ETFs-industries.csv"
output_csv = "/home/imagda/_invest2024/tradingview/watchlist/ETFs-industries-clustered.csv"
output_plot = "/home/imagda/_invest2024/tradingview/watchlist/cluster_plot.html"

def semantic_enrichment(df):
    """
    Enriches the description with domain knowledge to group related concepts.
    This helps TF-IDF bridge the gap between terms like 'Uranium' and 'Energy'.
    """
    mappings = {
        "energy": ["uranium", "nuclear", "oil", "gas", "solar", "power", "fuel", "cleantech", "renewables"],
        "technology": ["software", "cybersecurity", "semiconductor", "semi", "quantum", "robotics", "data", "internet", "tech"],
        "healthcare": ["biotech", "medical", "pharmaceutical", "generic", "healthcare", "devices", "neuroscience"],
        "finance": ["bank", "insurance", "financial", "investment", "trusts", "broker"],
        "materials": ["metal", "gold", "silver", "aluminum", "steel", "rare earth", "miners", "mining", "chemicals"],
        "industrials": ["aerospace", "defense", "machinery", "transportation", "freight", "airlines", "trucking", "shipping", "construction"],
        "consumer": ["retail", "apparel", "food", "beverages", "stores", "restaurants", "household", "gaming", "casinos"]
    }
    
    enriched_descriptions = []
    for _, row in df.iterrows():
        desc = row['Description'].lower()
        tags = []
        for sector, keywords in mappings.items():
            if any(kw in desc for kw in keywords):
                tags.append(sector)
        
        # Combine original description with sector tags for better semantic weight
        enriched = desc + " " + " ".join(tags)
        enriched_descriptions.append(enriched)
    
    return enriched_descriptions

def perform_clustering():
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    # 1. Load Data
    df = pd.read_csv(input_file)
    print(f"Loaded {len(df)} ETFs.")

    # 2. Preprocess & Vectorize
    enriched = semantic_enrichment(df)
    vectorizer = TfidfVectorizer(max_features=100)
    X = vectorizer.fit_transform(enriched).toarray()

    # 3. Dimensionality Reduction (PCA)
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    df['Dim1'] = X_pca[:, 0]
    df['Dim2'] = X_pca[:, 1]

    # 4. Hybrid Clustering
    # Step A: Hierarchical to get initial clusters and centroids
    n_clusters = 8
    hierarchical = AgglomerativeClustering(n_clusters=n_clusters)
    hier_labels = hierarchical.fit_predict(X)
    
    # Calculate centroids from hierarchical clustering
    initial_centroids = []
    for i in range(n_clusters):
        initial_centroids.append(X[hier_labels == i].mean(axis=0))
    initial_centroids = np.array(initial_centroids)

    # Step B: Refine with K-means
    kmeans = KMeans(n_clusters=n_clusters, init=initial_centroids, n_init=1)
    df['Cluster_ID'] = kmeans.fit_predict(X)
    
    # 5. Assign Cluster Names
    cluster_names = {
        0: "Financials & Insurance",
        1: "Materials & Mining",
        2: "Utilities & Infrastructure",
        3: "Energy & Power",
        4: "Consumer & Retail",
        5: "Technology & Innovation",
        6: "Healthcare & Life Sciences",
        7: "Industrial & Aerospace"
    }
    df['Cluster_Name'] = df['Cluster_ID'].map(cluster_names)

    # 6. Visualization
    fig = px.scatter(
        df, x='Dim1', y='Dim2',
        color='Cluster_Name',
        text='Symbol',
        hover_data=['Description', 'Cluster'],
        title='ETF Industries: Semantic Clustering (Named Zones)',
        template='plotly_dark'
    )
    
    fig.update_traces(textposition='top center')
    fig.update_layout(
        showlegend=True,
        legend_title_text='Cluster',
        xaxis_title='Semantic Dimension 1',
        yaxis_title='Semantic Dimension 2'
    )

    # 6. Save results
    df.to_csv(output_csv, index=False)
    fig.write_html(output_plot)
    print(f"CSV saved to {output_csv}")
    print(f"Plot saved to {output_plot}")

if __name__ == "__main__":
    perform_clustering()
