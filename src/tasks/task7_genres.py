import pandas as pd

def run(df: pd.DataFrame, plot: bool = False):
    print("\nRunning Task 7: Genre Statistics...")
    
    s = df['genres'].astype(str).str.split('|').explode()
    s = s[s != 'nan']
    s = s[s != '']
    genre_counts = s.value_counts()
    
    print(genre_counts.head(5))
    
    if plot:
        print(" -> Generating Genre Chart...")
        from src.visualization import plot_genre_counts
        plot_genre_counts(genre_counts)
