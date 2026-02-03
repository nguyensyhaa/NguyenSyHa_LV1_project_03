import pandas as pd

def run(df: pd.DataFrame, plot: bool = False):
    print("\nRunning Task 8: ROI Analysis...")
    
    df_calc = df[df['budget'] > 10000].copy()
    df_calc['roi'] = (df_calc['revenue'] - df_calc['budget']) / df_calc['budget']
    top_roi = df_calc.sort_values(by='roi', ascending=False).head(5)
    
    for _, row in top_roi.iterrows():
         print(f"    {row['original_title']} | ROI: {row['roi']:.2f}x")
            
    if plot:
        print(" -> Generating ROI Chart...")
        from src.visualization import plot_roi
        plot_roi(top_roi)
