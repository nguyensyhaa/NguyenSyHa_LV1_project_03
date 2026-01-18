import pandas as pd

def run(df: pd.DataFrame, plot: bool = False):
    print("\nRunning Task 3: Revenue Extremes...")
    
    # Max
    max_idx = df['revenue'].idxmax()
    max_movie = df.loc[max_idx]
    
    # Min (Filtering out 0)
    non_zero = df[df['revenue'] > 0]
    
    print(f" -> Highest: {max_movie['original_title']} (${max_movie['revenue']:,.0f})")
    
    if not non_zero.empty:
        min_val = non_zero['revenue'].min()
        all_min_movies = non_zero[non_zero['revenue'] == min_val]
        for _, m in all_min_movies.iterrows():
            print(f" -> Lowest:  {m['original_title']} (${m['revenue']:,.0f})")
            
    # Chart logic could be added here (e.g., Boxplot of Revenue) but keeping it simple for now as requested.
