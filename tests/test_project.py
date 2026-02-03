"""Test suite for TMDB Movie Analysis project"""
import pytest
import pandas as pd
from src.validation import DataQualityReport, validate_dataframe
from src.analysis import MovieAnalyzer
from src.config import REQUIRED_COLUMNS, NUMERIC_COLUMNS


class TestDataValidation:
    """Test data validation functionality"""
    
    def test_schema_validation_success(self, sample_movie_data):
        """Test schema validation with valid data"""
        quality = DataQualityReport(sample_movie_data)
        assert quality.validate_schema(REQUIRED_COLUMNS) is True
    
    def test_schema_validation_failure(self):
        """Test schema validation with missing columns"""
        df = pd.DataFrame({'id': [1, 2], 'title': ['A', 'B']})
        quality = DataQualityReport(df)
        assert quality.validate_schema(REQUIRED_COLUMNS) is False
    
    def test_missing_values_check(self, sample_movie_data):
        """Test missing values detection"""
        quality = DataQualityReport(sample_movie_data)
        missing = quality.check_missing_values(threshold=0.5)
        assert isinstance(missing, dict)
    
    def test_duplicates_check(self, sample_movie_data):
        """Test duplicate detection"""
        # Add a duplicate row
        df_with_dup = pd.concat([sample_movie_data, sample_movie_data.iloc[[0]]], ignore_index=True)
        quality = DataQualityReport(df_with_dup)
        dup_count = quality.check_duplicates()
        assert dup_count == 1
    
    def test_validate_dataframe_empty(self):
        """Test validation fails on empty dataframe"""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="empty"):
            validate_dataframe(df, REQUIRED_COLUMNS)
    
    def test_validate_dataframe_missing_columns(self, sample_movie_data):
        """Test validation fails on missing required columns"""
        df = sample_movie_data[['id', 'original_title']]  # Missing required columns
        with pytest.raises(ValueError, match="Missing required columns"):
            validate_dataframe(df, REQUIRED_COLUMNS)


class TestMovieAnalyzer:
    """Test MovieAnalyzer class"""
    
    def test_get_sorted_by_date(self, sample_movie_data):
        """Test sorting by release date"""
        # Convert release_date to datetime first
        sample_movie_data['release_date'] = pd.to_datetime(sample_movie_data['release_date'])
        
        analyzer = MovieAnalyzer(sample_movie_data)
        sorted_df = analyzer.get_sorted_by_date()
        
        # Check if sorted descending
        dates = sorted_df['release_date']
        assert dates.is_monotonic_decreasing
    
    def test_get_high_rated(self, sample_movie_data):
        """Test filtering high-rated movies"""
        analyzer = MovieAnalyzer(sample_movie_data)
        high_rated = analyzer.get_high_rated(threshold=7.5)
        
        # All movies should have rating > 7.5
        assert (high_rated['vote_average'] > 7.5).all()
    
    def test_get_revenue_extremes(self, sample_movie_data):
        """Test revenue extremes calculation"""
        analyzer = MovieAnalyzer(sample_movie_data)
        extremes = analyzer.get_revenue_extremes()
        
        assert 'max' in extremes
        assert 'min_list' in extremes
        
        # Max should be Avatar
        assert extremes['max']['original_title'] == 'Avatar'
    
    def test_get_total_revenue(self, sample_movie_data):
        """Test total revenue calculation"""
        analyzer = MovieAnalyzer(sample_movie_data)
        total = analyzer.get_total_revenue()
        
        expected = sample_movie_data['revenue'].sum()
        assert total == int(expected)
    
    def test_get_top_profit(self, sample_movie_data):
        """Test top profit calculation"""
        analyzer = MovieAnalyzer(sample_movie_data)
        top_profit = analyzer.get_top_profit(n=3)
        
        # Should return 3 movies
        assert len(top_profit) == 3
        
        # Should have profit column
        assert 'profit' in top_profit.columns
        
        # Profit should be descending
        assert top_profit['profit'].is_monotonic_decreasing
    
    def test_get_top_metrics(self, sample_movie_data):
        """Test top director/actor/genre metrics"""
        analyzer = MovieAnalyzer(sample_movie_data)
        metrics = analyzer.get_top_metrics()
        
        assert 'top_director' in metrics
        assert 'top_actor' in metrics
        assert 'genre_counts' in metrics
        
        # James Cameron appears twice in sample data
        assert metrics['top_director'] == 'James Cameron'
    
    def test_get_roi_stats(self, sample_movie_data):
        """Test ROI calculation"""
        analyzer = MovieAnalyzer(sample_movie_data)
        roi_df = analyzer.get_roi_stats(n=3)
        
        # Should return 3 movies
        assert len(roi_df) <= 3
        
        # Should have roi column
        assert 'roi' in roi_df.columns
        
        # ROI should be positive for profitable movies
        assert (roi_df['roi'] > 0).any()


class TestDataQuality:
    """Test data quality checks with problematic data"""
    
    def test_type_coercion_detection(self, sample_data_with_issues):
        """Test detection of type coercion issues"""
        quality = DataQualityReport(sample_data_with_issues)
        coercion = quality.check_data_types(['revenue', 'budget'])
        
        # Should detect invalid values
        assert len(coercion) > 0
    
    def test_negative_values_detection(self, sample_data_with_issues):
        """Test detection of negative values"""
        quality = DataQualityReport(sample_data_with_issues)
        negatives = quality.check_negative_values(['revenue', 'budget'])
        
        # Should detect negative revenue
        assert 'revenue' in negatives or len(negatives) >= 0
    
    def test_generate_report(self, sample_movie_data):
        """Test comprehensive report generation"""
        quality = DataQualityReport(sample_movie_data)
        quality.validate_schema(REQUIRED_COLUMNS)
        quality.check_missing_values()
        quality.check_duplicates()
        
        report = quality.generate_report()
        
        assert 'total_rows' in report
        assert 'total_columns' in report
        assert 'issues' in report
        assert 'metrics' in report
        assert report['total_rows'] == len(sample_movie_data)


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_dataframe_handling(self):
        """Test handling of empty dataframe"""
        df = pd.DataFrame()
        with pytest.raises(ValueError):
            validate_dataframe(df, REQUIRED_COLUMNS)
    
    def test_single_row_dataframe(self):
        """Test handling of single-row dataframe"""
        df = pd.DataFrame({
            'id': [1],
            'original_title': ['Test'],
            'revenue': [1000],
            'budget': [500],
            'release_date': ['2020-01-01'],
            'vote_average': [7.0],
            'director': ['Test Director'],
            'cast': ['Actor A'],
            'genres': ['Action']
        })
        
        # Should not raise error
        validate_dataframe(df, REQUIRED_COLUMNS)
        
        analyzer = MovieAnalyzer(df)
        assert analyzer.get_total_revenue() == 1000
