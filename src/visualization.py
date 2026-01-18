import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from src.config import OUTPUT_DIR

def setup_style():
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))

def save_plot(filename: str):
    plots_dir = os.path.join(OUTPUT_DIR, 'plots')
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
    path = os.path.join(plots_dir, filename)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    print(f"Chart saved to: {path}")

def plot_genre_counts(genre_counts: pd.Series):
    """Generates a bar chart for Top 10 Genres."""
    setup_style()
    # Top 10 for better visualization
    top_10 = genre_counts.head(10)
    
    sns.barplot(x=top_10.values, y=top_10.index, palette="viridis")
    plt.title("Top 10 Movie Genres", fontsize=16)
    plt.xlabel("Number of Movies")
    plt.ylabel("Genre")
    
    save_plot("top_genres.png")

def plot_roi(roi_df: pd.DataFrame):
    """Generates a bar chart for Top ROI Movies."""
    setup_style()
    
    sns.barplot(x='roi', y='original_title', data=roi_df, palette="magma")
    plt.title("Top 5 Movies by Return on Investment (ROI)", fontsize=16)
    plt.xlabel("ROI (Times Budget)")
    plt.ylabel("Movie Title")
    
    save_plot("top_roi.png")

def plot_top_profit(profit_df: pd.DataFrame):
    """Task 5: Bar chart for Top Profit Movies."""
    setup_style()
    sns.barplot(x='profit', y='original_title', data=profit_df, palette="Greens_d")
    plt.title("Top 10 Most Profitable Movies", fontsize=16)
    plt.xlabel("Profit ($)")
    plt.ylabel("Movie Title")
    save_plot("top_profit.png")

def plot_top_metrics(director_name, director_count, actor_name, actor_count):
    """Task 6: Simple comparison chart for Top Talent."""
    setup_style()
    # Create a small dataframe for plotting
    data = {
        'Name': [director_name, actor_name],
        'Role': ['Top Director', 'Top Actor'],
        'Count': [director_count, actor_count]
    }
    df = pd.DataFrame(data)
    
    sns.barplot(x='Count', y='Name', hue='Role', data=df, palette="muted")
    plt.title("Most Frequent Director & Actor", fontsize=16)
    save_plot("top_talent.png")

def plot_year_distribution(year_counts: pd.Series):
    """Task 1: Line chart for movies per year."""
    setup_style()
    sns.lineplot(x=year_counts.index, y=year_counts.values, marker="o")
    plt.title("Movies Released per Year", fontsize=16)
    plt.xlabel("Year")
    plt.ylabel("Number of Movies")
    save_plot("movies_per_year.png")

def plot_rating_distribution(ratings: pd.Series):
    """Task 2: Histogram for vote average."""
    setup_style()
    sns.histplot(ratings, bins=20, kde=True, color="purple")
    plt.title("Distribution of Movie Ratings", fontsize=16)
    plt.xlabel("Vote Average")
    plt.ylabel("Frequency")
    save_plot("rating_distribution.png")


