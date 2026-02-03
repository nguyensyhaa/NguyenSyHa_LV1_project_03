import pandas as pd
import numpy as np
import sys

input_path = "tmdb-movies-custom-cleaned.csv"

def run_analysis():
    print("Loading data...")
    df = pd.read_csv(input_path)
    # Ensure date is datetime (it should be from cleaning, but good to be safe)
    df['release_date'] = pd.to_datetime(df['release_date'])

    # --- Task 1: Sort by release date (descending) ---
    print("\n--- Task 1: Sorting by release date ---")
    sorted_df = df.sort_values(by='release_date', ascending=False)
    sorted_df.to_csv("sorted_by_date.csv", index=False)
    print("Saved to sorted_by_date.csv")

    # --- Task 2: Filter by rating > 7.5 ---
    print("\n--- Task 2: Filter by rating > 7.5 ---")
    high_rated = df[df['vote_average'] > 7.5]
    high_rated.to_csv("high_rated_movies.csv", index=False)
    print(f"Found {len(high_rated)} movies. Saved to high_rated_movies.csv")

    # --- Task 3: Max/Min Revenue ---
    print("\n--- Task 3: Max/Min Revenue ---")
    # Exclude 0 revenue if that's the intention? Usually for these datasets 0 means unknown.
    # However, standard max/min usually includes all. Let's check if 0s should be ignored.
    # For now, we take absolute max/min of the column.
    max_rev_idx = df['revenue'].idxmax()
    min_rev_idx = df['revenue'].idxmin()
    
    print(f"Highest Revenue: {df.loc[max_rev_idx, 'original_title']} (${df.loc[max_rev_idx, 'revenue']:,.2f})")
    
    # Filter out 0 revenue for specific "Lowest Revenue" check, as 0 usually equates to missing/unknown
    non_zero_revenue = df[df['revenue'] > 0]
    if not non_zero_revenue.empty:
        min_rev_idx = non_zero_revenue['revenue'].idxmin()
        print(f"Lowest Revenue: {non_zero_revenue.loc[min_rev_idx, 'original_title']} (${non_zero_revenue.loc[min_rev_idx, 'revenue']:,.2f})")
    else:
        print("Lowest Revenue: $0.00 (All movies have 0 revenue)")


    # --- Task 4: Total Revenue ---
    print("\n--- Task 4: Total Revenue ---")
    total_revenue = df['revenue'].sum()
    print(f"Total Revenue: ${total_revenue:,.2f}")

    # --- Task 5: Top 10 Profit ---
    print("\n--- Task 5: Top 10 Profit ---")
    df['profit'] = df['revenue'] - df['budget']
    top_10_profit = df.sort_values(by='profit', ascending=False).head(10)
    print(top_10_profit[['original_title', 'profit', 'revenue', 'budget']].to_string(index=False))

    # --- Task 6: Top Director & Actor ---
    print("\n--- Task 6: Top Director & Actor ---")
    
    # Directors
    # Many rows have multiple directors separated by '|'. 
    # We need to split and count.
    directors = df['director'].str.split('|').explode()
    # Remove empty strings if any
    directors = directors[directors != '']
    top_director = directors.mode()[0]
    director_counts = directors.value_counts()
    print(f"Most frequent director: {top_director} ({director_counts[top_director]} movies)")

    # Actors (cast)
    cast = df['cast'].str.split('|').explode()
    cast = cast[cast != '']
    top_actor = cast.mode()[0]
    actor_counts = cast.value_counts()
    print(f"Most frequent actor: {top_actor} ({actor_counts[top_actor]} movies)")


    # --- Task 7: Genre Statistics ---
    print("\n--- Task 7: Genre Statistics ---")
    genres = df['genres'].str.split('|').explode()
    genres = genres[genres != '']
    genre_counts = genres.value_counts()
    print(genre_counts.to_string())

    # --- Task 8: Additional Analysis (Revenue per Year) ---
    print("\n--- Task 8: Additional Analysis - Avg Revenue per Year ---")
    df['year'] = df['release_date'].dt.year
    # Group by year, calc mean revenue, sort by year
    yearly_rev = df.groupby('year')['revenue'].mean()
    # Print last 5 years as sample
    print(yearly_rev.tail(5).to_string())
    
if __name__ == "__main__":
    run_analysis()
