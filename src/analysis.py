import pandas as pd
from typing import Dict, Any

class MovieAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_sorted_by_date(self) -> pd.DataFrame:
        """Task 1: Sort by release date descending."""
        # Create a parsed column for display/verification if needed, strictly to match reference format?
        # Reference output: release_date_parsed,id,... 
        # We can create a copy.
        result = self.df.sort_values(by='release_date', ascending=False).copy()
        
        # Add 'release_date_parsed' as first column (YYYY-MM-DD string) 
        # to match verify sample: 2015-12-31, ...
        # The reference shows first col as 'release_date_parsed'.
        result.insert(0, 'release_date_parsed', result['release_date'].dt.strftime('%Y-%m-%d'))
        
        return result

    def get_high_rated(self, threshold: float = 7.5) -> pd.DataFrame:
        """Task 2: Filter by rating > threshold."""
        return self.df[self.df['vote_average'] > threshold].copy()

    def get_revenue_extremes(self) -> Dict[str, Any]:
        """Task 3: Max and Min revenue."""
        # Max
        max_idx = self.df['revenue'].idxmax()
        max_movie = self.df.loc[max_idx]
        
        # Min (Filtering out 0)
        non_zero = self.df[self.df['revenue'] > 0]
        if non_zero.empty:
            min_movie = None
        else:
            min_idx = non_zero['revenue'].idxmin()
            min_movie = non_zero.loc[min_idx]
            
            # Check for multiple min movies (e.g. Mallrats AND Shattered Glass at $2)
            # The verify output shows two. Let's find all with the min value.
            min_val = min_movie['revenue']
            all_min_movies = non_zero[non_zero['revenue'] == min_val]
        
        return {
            'max': max_movie,
            'min_list': all_min_movies if not non_zero.empty else []
        }

    def get_total_revenue(self) -> int:
        """Task 4: Total Revenue."""
        return int(self.df['revenue'].sum())

    def get_top_profit(self, n: int = 10) -> pd.DataFrame:
        """Task 5: Top n profit."""
        # profit = revenue - budget
        # We assign it temporarily
        df_calc = self.df.copy()
        df_calc['profit'] = df_calc['revenue'] - df_calc['budget']
        return df_calc.sort_values(by='profit', ascending=False).head(n)

    def get_top_metrics(self) -> Dict[str, Any]:
        """Task 6 & 7: Top Director, Actor, Genre Counts."""
        # Helper to split and count
        def get_top_item(column: str):
            # Explode
            s = self.df[column].astype(str).str.split('|').explode()
            s = s[s != 'nan'] # Remove nan strings if any
            s = s[s != '']    # Remove empty
            return s.value_counts()

        directors = get_top_item('director')
        actors = get_top_item('cast')
        genres = get_top_item('genres')

        return {
            'top_director': directors.index[0] if not directors.empty else None,
            'top_director_count': directors.iloc[0] if not directors.empty else 0,
            'top_actor': actors.index[0] if not actors.empty else None,
            'top_actor_count': actors.iloc[0] if not actors.empty else 0,
            'genre_counts': genres
        }

    def get_roi_stats(self, n: int = 5) -> pd.DataFrame:
        """Task 8: Return on Investment (ROI) Analysis.
        ROI = (Revenue - Budget) / Budget
        Filters: Budget > MIN_BUDGET_FOR_ROI to avoid skewed results from near-zero budget indie films/errors.
        """
        from src.config import MIN_BUDGET_FOR_ROI
        
        # Filter reasonable budget to avoid division by zero or massive outliers on $1 budget
        df_calc = self.df[self.df['budget'] > MIN_BUDGET_FOR_ROI].copy()
        
        # Calculate ROI
        df_calc['roi'] = (df_calc['revenue'] - df_calc['budget']) / df_calc['budget']
        
        return df_calc.sort_values(by='roi', ascending=False).head(n)



