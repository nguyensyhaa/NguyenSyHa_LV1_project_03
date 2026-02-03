import pandas as pd
import os
from src.config import OUTPUT_DIR

def run(df: pd.DataFrame, plot: bool = False):
    print("Running Task 1: Sorting by Release Date...")
    
    # Logic
    df_sorted = df.sort_values(by='release_date', ascending=False).copy()
    
    # Save output
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    sorted_path = os.path.join(OUTPUT_DIR, "sorted_by_date.csv")
    df_sorted.to_csv(sorted_path, index=False)
    print(f" -> Saved {len(df_sorted)} rows to {sorted_path}")
    
    # Visualization: Movies per Year
    if plot:
        print(" -> Generating Year Distribution Chart...")
        from src.visualization import plot_year_distribution
        # Count movies per year
        year_counts = df['release_date'].dt.year.value_counts().sort_index()
        plot_year_distribution(year_counts)
    
    return df_sorted
