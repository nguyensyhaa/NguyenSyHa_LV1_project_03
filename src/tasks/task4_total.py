import pandas as pd

def run(df: pd.DataFrame, plot: bool = False):
    print("\nRunning Task 4: Total Revenue...")
    
    total_rev = int(df['revenue'].sum())
    print(f" -> Total: ${total_rev:,.0f}")
