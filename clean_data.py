import pandas as pd
import numpy as np

input_path = "tmdb-movies.csv"
output_path = "tmdb-movies-cleaned.csv"

def clean_data(input_path, output_path):
    print(f"Loading data from {input_path}...")
    try:
        df = pd.read_csv(input_path)
    except Exception as e:
        print(f"Error reading {input_path}: {e}")
        return

    print(f"Original shape: {df.shape}")

    # 1. Duplicates
    # NOTE: The reference implementation (Project 01 Linux) likely includes duplicates.
    # To match the output numbers exactly (e.g. Total Revenue, Genre Counts), we will NOT remove duplicates.
    # if df.duplicated().sum() > 0:
    #     print(f"Found {df.duplicated().sum()} duplicates. Removing...")
    #     df.drop_duplicates(inplace=True)

    
    # 2. Convert Release Date
    # errors='coerce' turns invalid parsing into NaT
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    
    # FIX: Handle 2-digit years interpreted as future
    # e.g. 60 becomes 2060 instead of 1960
    current_year = pd.Timestamp.now().year
    # Let's use a safe cutoff, e.g. next year to allow for very recent data
    future_mask = df['release_date'].dt.year > (current_year + 1)
    if future_mask.sum() > 0:
        print(f"Fixing {future_mask.sum()} dates that were parsed as future years...")
        df.loc[future_mask, 'release_date'] = df.loc[future_mask, 'release_date'] - pd.DateOffset(years=100)

    
    # 3. Numeric conversions
    numeric_cols = ['popularity', 'budget', 'revenue', 'runtime', 'vote_count', 'vote_average']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 4. Handle Delimiters (just ensuring they are strings)
    string_cols = ['cast', 'homepage', 'director', 'tagline', 'keywords', 'overview', 'genres', 'production_companies']
    for col in string_cols:
        df[col] = df[col].astype(str).replace('nan', '')

    # 5. Drop rows with critical missing info (if any relevant analysis depends on it)
    # For this project, we might just keep them but be aware.
    # checking NaT in release_date
    na_dates = df['release_date'].isna().sum()
    if na_dates > 0:
        print(f"Warning: {na_dates} rows have invalid release_date.")
    
    print(f"Cleaned shape: {df.shape}")
    
    df.to_csv(output_path, index=False)
    print(f"Saved cleaned data to {output_path}")

if __name__ == "__main__":
    clean_data(input_path, output_path)
