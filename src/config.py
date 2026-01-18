import os

# URLs
DATA_URL = "https://raw.githubusercontent.com/yinghaoz1/tmdb-movie-dataset-analysis/master/tmdb-movies.csv"

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')

# Constants
MIN_VOTE_AVERAGE = 7.5
CURRENT_YEAR_THRESHOLD = 2026 # To detect 2-digit year errors (e.g. 2060 -> 1960)
