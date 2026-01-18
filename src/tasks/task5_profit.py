import pandas as pd

def run(df: pd.DataFrame, plot: bool = False):
    print("\nRunning Task 5: Top 10 Profit...")
    
    # Logic
    df_calc = df.copy()
    df_calc['profit'] = df_calc['revenue'] - df_calc['budget']
    top_profit = df_calc.sort_values(by='profit', ascending=False).head(10)
    
    for i, row in top_profit.iterrows():
        print(f"    {row['original_title']} | ${int(row['profit']):,.0f}")
    
    # Visualization
    if plot:
        print(" -> Generating Profit Chart...")
        from src.visualization import plot_top_profit
        plot_top_profit(top_profit)
