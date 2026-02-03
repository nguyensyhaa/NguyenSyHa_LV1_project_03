import pandas as pd
import os
from src.config import OUTPUT_DIR

def run(df: pd.DataFrame, plot: bool = False):
    print("\nRunning Task 2: Filtering (>7.5)...")
    
    # Logic
    df_high = df[df['vote_average'] > 7.5].copy()
    
    # Save output
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    high_path = os.path.join(OUTPUT_DIR, "high_rated_movies.csv")

    df_high.to_csv(high_path, index=False)
    print(f" -> Found {len(df_high)} movies. Saved to {high_path}")
    
    # Visualization: Rating Distribution
    if plot:
        print(" -> Generating Rating Distribution Chart...")
        from src.visualization import plot_rating_distribution
        plot_rating_distribution(df['vote_average'])
        
    return df_high
