import time
import pandas as pd
from custom_clean_data import custom_parser

input_path = "tmdb-movies.csv"

def benchmark_custom():
    start = time.time()
    # Run the custom parser logic (from the user's algorithm)
    data = custom_parser(input_path)
    columns = data[0]
    rows = data[1:]
    df = pd.DataFrame(rows, columns=columns)
    
    # Custom cleaning steps (same as before)
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    current_year = pd.Timestamp.now().year
    future_mask = df['release_date'].dt.year > (current_year + 1)
    if future_mask.sum() > 0:
        df.loc[future_mask, 'release_date'] = df.loc[future_mask, 'release_date'] - pd.DateOffset(years=100)
        
    numeric_cols = ['popularity', 'budget', 'revenue', 'runtime', 'vote_count', 'vote_average']
    for col in numeric_cols:
         df[col] = pd.to_numeric(df[col], errors='coerce')
         
    end = time.time()
    print(f"Custom Parser Time: {end - start:.4f} seconds")
    return df

def benchmark_pandas_optimized():
    start = time.time()
    # Pandas C-engine parser
    # It automatically handles newlines inside quotes.
    df = pd.read_csv(input_path)
    
    # Vectorized cleanup to match the "remove newline" logic
    # Apply to object columns only for efficiency
    obj_cols = df.select_dtypes(include=['object']).columns
    df[obj_cols] = df[obj_cols].replace(r'\n', ' ', regex=True)
    
    # Vectorized date fix
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    current_year = pd.Timestamp.now().year
    # Fast boolean indexing
    future_mask = df['release_date'].dt.year > (current_year + 1)
    # Using loc is efficient enough, or we could use np.where
    df.loc[future_mask, 'release_date'] = df.loc[future_mask, 'release_date'] - pd.DateOffset(years=100)
    
    # Numerics are already handled by read_csv mostly, but to be safe/explicit:
    # read_csv usually infers types well, but let's force strictness if needed.
    # Actually read_csv is faster at inference.
    
    end = time.time()
    print(f"Pandas Optimized Time: {end - start:.4f} seconds")
    return df

if __name__ == "__main__":
    print(f"Benchmarking on {input_path}...")
    df_custom = benchmark_custom()
    df_pandas = benchmark_pandas_optimized()
    
    print(f"\nShape Match: {df_custom.shape == df_pandas.shape}")
    print(f"Custom Shape: {df_custom.shape}")
    print(f"Pandas Shape: {df_pandas.shape}")
    
    # Check if Total Revenue matches
    rev_custom = df_custom['revenue'].sum()
    rev_pandas = df_pandas['revenue'].sum()
    print(f"Revenue Difference: {abs(rev_custom - rev_pandas)}")
