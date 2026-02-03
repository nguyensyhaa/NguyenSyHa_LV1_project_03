"""Configuration constants for TMDB Movie Analysis"""
import os

# Data Source
DATA_URL = "https://raw.githubusercontent.com/yinghaoz1/tmdb-movie-dataset-analysis/master/tmdb-movies.csv"

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')

# Analysis Parameters
MIN_VOTE_AVERAGE = 7.5  # Threshold for high-rated movies (Task 2)
CURRENT_YEAR_THRESHOLD = 2026  # To detect 2-digit year parsing errors (e.g. 2060 -> 1960)
MIN_BUDGET_FOR_ROI = 10000  # Minimum budget to avoid division by zero and indie film outliers (Task 8)

# Data Quality Thresholds
MISSING_VALUE_WARNING_THRESHOLD = 0.5  # Warn if column has >50% missing values
MIN_VALID_YEAR = 1900  # Minimum valid release year
MAX_VALID_YEAR = 2026  # Maximum valid release year

# Expected Schema
REQUIRED_COLUMNS = [
    'id', 'original_title', 'revenue', 'budget', 
    'release_date', 'vote_average', 'director', 
    'cast', 'genres'
]

NUMERIC_COLUMNS = [
    'popularity', 'budget', 'revenue', 'runtime', 
    'vote_count', 'vote_average'
]

POSITIVE_VALUE_COLUMNS = [
    'budget', 'revenue', 'runtime', 'vote_count'
]


def validate_config() -> None:
    """Validate configuration values"""
    if CURRENT_YEAR_THRESHOLD < 2020:
        raise ValueError(f"CURRENT_YEAR_THRESHOLD ({CURRENT_YEAR_THRESHOLD}) is too old")
    
    if not (0 <= MIN_VOTE_AVERAGE <= 10):
        raise ValueError(f"MIN_VOTE_AVERAGE must be 0-10, got {MIN_VOTE_AVERAGE}")
    
    if MIN_BUDGET_FOR_ROI < 0:
        raise ValueError(f"MIN_BUDGET_FOR_ROI must be positive, got {MIN_BUDGET_FOR_ROI}")
    
    if not (0 <= MISSING_VALUE_WARNING_THRESHOLD <= 1):
        raise ValueError(f"MISSING_VALUE_WARNING_THRESHOLD must be 0-1, got {MISSING_VALUE_WARNING_THRESHOLD}")

