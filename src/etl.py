import pandas as pd
import numpy as np
from src.config import CURRENT_YEAR_THRESHOLD

def load_data(source_url_or_path: str) -> pd.DataFrame:
    """
    Loads data from a URL or local path using optimized Pandas C-engine.
    Performs streaming download if URL is provided.
    """
    print(f"Loading data from {source_url_or_path}...")
    try:
        # Pandas read_csv handles URLs natively
        df = pd.read_csv(source_url_or_path)
        return df
    except Exception as e:
        raise RuntimeError(f"Failed to load data from {source_url_or_path}: {e}")

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the dataframe:
    1. Fixes newlines in string columns (vectorized).
    2. Parses dates and fixes 2-digit years (e.g. 60 -> 1960).
    3. Ensures numeric columns are typed correctly.
    
    NOTE: Does NOT drop duplicates, to match legacy reference values (Total Revenue ~432B).
    """
    # 1. Vectorized cleanup of newlines inside string columns
    # Select object columns that are likely to contain messy text
    obj_cols = df.select_dtypes(include=['object']).columns
    # Only replace if strictly needed, but 'replace' with regex is generally fast enough
    df[obj_cols] = df[obj_cols].replace(r'\n', ' ', regex=True)

    # 2. Date Parsing & Fix
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    
    # Fix future years (e.g. 2060 -> 1960)
    # Using config threshold
    future_mask = df['release_date'].dt.year > CURRENT_YEAR_THRESHOLD
    if future_mask.sum() > 0:
        print(f"  Fixing {future_mask.sum()} dates interpreted as future years (>{CURRENT_YEAR_THRESHOLD}).")
        df.loc[future_mask, 'release_date'] = df.loc[future_mask, 'release_date'] - pd.DateOffset(years=100)

    # 3. Numeric Conversions 
    # (read_csv does this well, but let's ensure specific key columns are numeric)
    numeric_cols = ['popularity', 'budget', 'revenue', 'runtime', 'vote_count', 'vote_average'] 
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 4. Fill NaNs in numeric columns if needed? 
    # For now, we leave them as NaN or 0 depending on analysis needs.
    # Usually revenue=0 is kept as 0. 

    return df
