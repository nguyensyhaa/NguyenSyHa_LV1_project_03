import pandas as pd

def run(df: pd.DataFrame, plot: bool = False):
    print("\nRunning Task 6: Top Talent...")
    
    def get_top_item(column: str):
        # Explode logic
        s = df[column].astype(str).str.split('|').explode()
        s = s[s != 'nan']
        s = s[s != '']
        return s.value_counts()

    directors = get_top_item('director')
    actors = get_top_item('cast')
    
    top_dir = directors.index[0] if not directors.empty else None
    top_dir_count = directors.iloc[0] if not directors.empty else 0
    top_act = actors.index[0] if not actors.empty else None
    top_act_count = actors.iloc[0] if not actors.empty else 0

    print(f" -> Director: {top_dir} ({top_dir_count})")
    print(f" -> Actor:    {top_act} ({top_act_count})")

    if plot:
        print(" -> Generating Talent Chart...")
        from src.visualization import plot_top_metrics
        plot_top_metrics(top_dir, top_dir_count, top_act, top_act_count)
