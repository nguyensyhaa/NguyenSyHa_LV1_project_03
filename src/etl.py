"""ETL (Extract, Transform, Load) module for TMDB movie data"""
import pandas as pd
import logging
from typing import Optional
from src.config import (
    CURRENT_YEAR_THRESHOLD, NUMERIC_COLUMNS, 
    REQUIRED_COLUMNS, POSITIVE_VALUE_COLUMNS,
    MIN_VALID_YEAR, MAX_VALID_YEAR,
    MISSING_VALUE_WARNING_THRESHOLD
)
from src.validation import DataQualityReport, validate_dataframe
from src.data_issues_tracker import DataIssuesTracker

logger = logging.getLogger(__name__)


def load_data(source_url: str, engine: Optional[str] = None) -> pd.DataFrame:
    """
    Load data from URL using Pandas with fallback mechanism
    
    Strategy:
    1. Try C-engine first (default, usually faster for well-formed CSV)
    2. If C-engine fails, fallback to Python engine (more robust)
    3. If both fail, raise error
    
    Args:
        source_url: URL to CSV data source
        engine: Force specific engine ('c' or 'python'). If None, auto-select with fallback
        
    Returns:
        Raw DataFrame
        
    Raises:
        RuntimeError: If data loading fails with both engines
    """
    logger.info(f"Loading data from: {source_url}")
    
    # If engine is specified, use it directly
    if engine:
        logger.info(f"Using specified engine: {engine}")
        try:
            df = pd.read_csv(source_url, engine=engine)
            logger.info(f"Successfully loaded {len(df)} rows, {len(df.columns)} columns")
            return df
        except Exception as e:
            logger.error(f"Failed to load with {engine} engine: {e}")
            raise RuntimeError(f"Data loading failed with {engine} engine: {e}")
    
    # Auto-select with fallback
    # Try C-engine first (default, usually faster)
    try:
        logger.info("Attempting to load with C-engine...")
        df = pd.read_csv(source_url, engine='c')
        logger.info(f"✓ C-engine successful: {len(df)} rows, {len(df.columns)} columns")
        return df
        
    except Exception as e_c:
        logger.warning(f"C-engine failed: {e_c}")
        logger.info("Falling back to Python engine...")
        
        # Fallback to Python engine (more robust, handles edge cases better)
        try:
            df = pd.read_csv(source_url, engine='python')
            logger.info(f"✓ Python engine successful: {len(df)} rows, {len(df.columns)} columns")
            logger.warning("Note: Used Python engine fallback (slower but more robust)")
            return df
            
        except Exception as e_py:
            logger.error(f"Python engine also failed: {e_py}")
            raise RuntimeError(
                f"Data loading failed with both engines.\n"
                f"  C-engine error: {e_c}\n"
                f"  Python engine error: {e_py}"
            )


def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean text columns by removing newlines
    
    Args:
        df: DataFrame to clean
        
    Returns:
        DataFrame with cleaned text
    """
    obj_cols = df.select_dtypes(include=['object']).columns
    logger.info(f"Cleaning {len(obj_cols)} text columns")
    df[obj_cols] = df[obj_cols].replace(r'\n', ' ', regex=True)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate the dataframe
    
    SAVES ALL BAD DATA TO outputs/data_issues.json (single file)
    
    Steps:
    1. Quick validation (schema check)
    2. Clean text columns
    3. Fix date parsing errors (track issues)
    4. Convert numeric columns (track coerced values)
    5. Track duplicates
    6. Save all issues to JSON
    7. Run quality checks
    
    Args:
        df: Raw DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    logger.info("=" * 60)
    logger.info("Starting data cleaning pipeline")
    logger.info("=" * 60)
    
    # Initialize issues tracker
    tracker = DataIssuesTracker()
    
    # Step 1: Quick validation
    logger.info("Step 1: Schema validation")
    validate_dataframe(df, REQUIRED_COLUMNS)
    
    # Step 2: Clean text
    logger.info("Step 2: Cleaning text columns")
    df = clean_text_columns(df)
    
    # Step 3: Fix dates (Pandas parsing issue, NOT bad data)
    logger.info("Step 3: Fixing date parsing errors")
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    future_mask = df['release_date'].dt.year > CURRENT_YEAR_THRESHOLD
    
    if future_mask.sum() > 0:
        # Không track - đây là lỗi parse của Pandas, data gốc không sai
        logger.warning(f"Fixing {future_mask.sum()} dates (2-digit year parsing: 60->2060 should be 1960)")
        df.loc[future_mask, 'release_date'] = (
            df.loc[future_mask, 'release_date'] - pd.DateOffset(years=100)
        )
        logger.info(f"Successfully fixed {future_mask.sum()} future dates")
    
    # Step 4: Convert numerics (with tracking)
    logger.info("Step 4: Converting numeric columns")
    total_coerced = 0
    
    for col in NUMERIC_COLUMNS:
        if col not in df.columns:
            continue
        
        original_values = df[col].copy()
        before_count = df[col].notna().sum()
        
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
        after_count = df[col].notna().sum()
        coerced = before_count - after_count
        
        if coerced > 0:
            total_coerced += coerced
            coerced_mask = original_values.notna() & df[col].isna()
            tracker.add_coerced_values(df, col, original_values, coerced_mask)
            logger.warning(f"Column '{col}': {coerced} values coerced to NaN")
    
    if total_coerced > 0:
        logger.warning(f"Total values coerced to NaN: {total_coerced}")
    else:
        logger.info("All numeric columns converted without coercion")
    
    # Step 5: Track duplicates (không xóa)
    dup_mask = df.duplicated()
    if dup_mask.sum() > 0:
        tracker.add_duplicates(df, dup_mask)
        logger.info(f"Found {dup_mask.sum()} duplicates (keeping for reference)")
    
    # Save all tracked issues to single JSON
    tracker.save()
    
    # Step 6: Comprehensive quality check
    logger.info("Step 6: Running comprehensive data quality checks")
    quality = DataQualityReport(df)
    
    quality.validate_schema(REQUIRED_COLUMNS)
    quality.check_missing_values(threshold=MISSING_VALUE_WARNING_THRESHOLD)
    quality.check_duplicates()
    quality.check_data_types(NUMERIC_COLUMNS)
    quality.check_date_range('release_date', MIN_VALID_YEAR, MAX_VALID_YEAR)
    quality.check_negative_values(POSITIVE_VALUE_COLUMNS)
    
    report = quality.generate_report()
    quality.save_report()
    
    logger.info("=" * 60)
    logger.info(f"Data cleaning complete: {report['issues_count']} issues found")
    logger.info(f"Final shape: {len(df)} rows × {len(df.columns)} columns")
    logger.info("=" * 60)
    
    return df


def profile_data(df: pd.DataFrame) -> None:
    """
    Generate and log data profiling summary
    
    Args:
        df: DataFrame to profile
    """
    logger.info("\n" + "=" * 60)
    logger.info("DATA PROFILING SUMMARY")
    logger.info("=" * 60)
    
    logger.info(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    
    # Missing values
    missing_pct = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)
    missing_cols = missing_pct[missing_pct > 0]
    
    if not missing_cols.empty:
        logger.info(f"\nMissing Values (top 5):")
        for col, pct in missing_cols.head(5).items():
            logger.info(f"  {col}: {pct:.1f}%")
    
    # Date range
    if 'release_date' in df.columns:
        logger.info(f"\nRelease Date Range:")
        logger.info(f"  Earliest: {df['release_date'].min()}")
        logger.info(f"  Latest: {df['release_date'].max()}")
    
    # Numeric summaries
    if 'revenue' in df.columns:
        logger.info(f"\nRevenue Statistics:")
        logger.info(f"  Total: ${df['revenue'].sum():,.0f}")
        logger.info(f"  Mean: ${df['revenue'].mean():,.0f}")
        logger.info(f"  Median: ${df['revenue'].median():,.0f}")
    
    logger.info("=" * 60 + "\n")
