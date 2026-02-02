# TMDB Movie Analysis

Data Engineering project analyzing TMDB movie dataset using Pandas.

## Installation

```bash
# Install Poetry (if not already installed)
pip install poetry

# Install project dependencies
poetry install

# Activate virtual environment
poetry shell
```

## Usage

**Run all tasks:**
```bash
python main.py
```

**Run specific task:**
```bash
python main.py --task 1  # Task 1: Sort by date
python main.py --task 2  # Task 2: Filter high-rated movies
python main.py --task 5  # Task 5: Top profit analysis
```

**Generate visualizations:**
```bash
python main.py --plot              # All tasks with charts
python main.py --task 5 --plot     # Task 5 with chart
```

**Enable debug logging:**
```bash
python main.py --debug
```

**Run tests:**
```bash
poetry run pytest
poetry run pytest --cov=src  # With coverage
```

## Output

Results are saved to `outputs/`:
- **CSV files:** `sorted_by_date.csv`, `high_rated_movies.csv`
- **Visualizations:** `plots/` directory
- **Logs:** `logs/tmdb_analysis.log`
- **Data quality report:** `data_quality_report.json`
- **Data issues:** `data_issues.json` (all bad data - original values only)

## Project Structure

```
src/
├── config.py           # Configuration constants
├── logging_config.py   # Logging setup
├── validation.py       # Data quality checks
├── etl.py              # Data loading & cleaning
├── analysis.py         # Analysis logic
├── visualization.py    # Plotting functions
└── tasks/              # Task modules (1-8)
```

## Tasks

1. Sort movies by release date
2. Filter high-rated movies (rating > 7.5)
3. Find revenue extremes (max/min)
4. Calculate total revenue
5. Top 10 most profitable movies
6. Most frequent director & actor
7. Top genres distribution
8. ROI (Return on Investment) analysis