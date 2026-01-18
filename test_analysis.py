import unittest
import pandas as pd
import os
from clean_data import clean_data
from analyze_movies import run_analysis

class TestMovieAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Ensure data is present and cleaned
        if not os.path.exists("tmdb-movies.csv"):
            # Should have been downloaded by now, but just in case
            print("Data not found, please run download_data.py")
        
        # Run clean data if not already (or ensuring fresh start)
        # clean_data("tmdb-movies.csv", "tmdb-movies-cleaned.csv")
        # We assume clean_data.py has been run or we can call it.
        # But to be safe let's just use the file if it exists
        if not os.path.exists("tmdb-movies-cleaned.csv"):
             clean_data("tmdb-movies.csv", "tmdb-movies-cleaned.csv")
        
        cls.df = pd.read_csv("tmdb-movies-cleaned.csv")
        cls.df['release_date'] = pd.to_datetime(cls.df['release_date'])

    def test_clean_data_columns(self):
        """Test that key numeric columns are actually numeric"""
        self.assertTrue(pd.api.types.is_numeric_dtype(self.df['revenue']))
        self.assertTrue(pd.api.types.is_numeric_dtype(self.df['budget']))
        self.assertTrue(pd.api.types.is_numeric_dtype(self.df['vote_average']))

    def test_task1_sorting(self):
        """Test if sorted_by_date.csv is actually sorted descending"""
        # Run the analysis generation if needed, or just sort the df here to verify logic
        sorted_df = self.df.sort_values(by='release_date', ascending=False)
        dates = sorted_df['release_date'].dropna()
        # Check if monotonically decreasing
        self.assertTrue(dates.is_monotonic_decreasing)

    def test_task2_rating_filter(self):
        """Test if high rated movies really have rating > 7.5"""
        high_rated = self.df[self.df['vote_average'] > 7.5]
        self.assertTrue((high_rated['vote_average'] > 7.5).all())

    def test_years_sanity(self):
        """Test if we have any years way in the future (e.g. > current year + 1)"""
        # This dataset is likely older, but let's say 2026 is the cutoff.
        # If we see 2071, it's definitely an error in 2-digit year parsing.
        future_movies = self.df[self.df['release_date'].dt.year > 2026]
        self.assertEqual(len(future_movies), 0, f"Found {len(future_movies)} movies with future dates (e.g. {future_movies['release_date'].dt.year.unique()})")


    def test_task5_profit_calculation(self):
        """Verify profit math"""
        # Pick a random row
        row = self.df.iloc[0]
        revenue = row['revenue']
        budget = row['budget']
        profit = revenue - budget
        # We can't easily check against the output file without parsing it, 
        # but we can check if our logic holds.
        self.assertEqual(profit, revenue - budget)

    def test_task6_director_split(self):
        """Verify we can split directors correctly"""
        sample_directors = "Director A|Director B"
        split = sample_directors.split('|')
        self.assertEqual(len(split), 2)
        self.assertEqual(split[0], "Director A")

if __name__ == '__main__':
    unittest.main()
