"""Pytest configuration and fixtures"""
import pytest
import pandas as pd
from datetime import datetime


@pytest.fixture
def sample_movie_data():
    """Sample movie data for testing"""
    return pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'imdb_id': ['tt0001', 'tt0002', 'tt0003', 'tt0004', 'tt0005'],
        'original_title': ['Avatar', 'Titanic', 'The Avengers', 'Jurassic World', 'Furious 7'],
        'revenue': [2787965087, 2187463944, 1518812988, 1671713208, 1516045911],
        'budget': [237000000, 200000000, 220000000, 150000000, 190000000],
        'vote_average': [7.2, 7.8, 7.7, 6.9, 7.3],
        'vote_count': [11800, 9100, 12000, 8500, 6200],
        'release_date': ['2009-12-10', '1997-11-18', '2012-04-25', '2015-06-09', '2015-04-01'],
        'director': ['James Cameron', 'James Cameron', 'Joss Whedon', 'Colin Trevorrow', 'James Wan'],
        'cast': ['Sam Worthington|Zoe Saldana', 'Leonardo DiCaprio|Kate Winslet', 
                 'Robert Downey Jr.|Chris Evans', 'Chris Pratt|Bryce Dallas Howard',
                 'Vin Diesel|Paul Walker'],
        'genres': ['Action|Adventure|Fantasy', 'Drama|Romance', 'Action|Adventure|Sci-Fi',
                   'Action|Adventure|Sci-Fi', 'Action|Crime|Thriller'],
        'popularity': [150.437577, 123.456789, 134.567890, 98.765432, 87.654321],
        'runtime': [162, 194, 143, 124, 137],
        'homepage': ['http://www.avatarmovie.com/', 'http://www.titanicmovie.com/', '', '', ''],
        'tagline': ['Enter the World', 'Nothing on Earth could come between them', 
                    'Some assembly required', 'The park is open', 'Vengeance hits home'],
        'keywords': ['future|marine|native', 'ship|iceberg|love', 'superhero|team|alien',
                     'dinosaur|park|island', 'car|racing|revenge'],
        'overview': ['A paraplegic marine...', 'A seventeen-year-old aristocrat...', 
                     'When an unexpected enemy...', 'Twenty-two years after...', 
                     'Continuing the global...'],
        'production_companies': ['Lightstorm Entertainment', '20th Century Fox|Paramount Pictures',
                                 'Marvel Studios', 'Universal Pictures|Legendary Pictures',
                                 'Universal Pictures'],
        'release_year': [2009, 1997, 2012, 2015, 2015],
        'budget_adj': [237000000.0, 200000000.0, 220000000.0, 150000000.0, 190000000.0],
        'revenue_adj': [2787965087.0, 2187463944.0, 1518812988.0, 1671713208.0, 1516045911.0]
    })


@pytest.fixture
def sample_data_with_issues():
    """Sample data with quality issues for testing validation"""
    return pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'original_title': ['Movie A', 'Movie B', 'Movie C', 'Movie D', 'Movie E'],
        'revenue': [1000000, 'invalid', 500000, -100, 0],  # Invalid and negative values
        'budget': [500000, 1000000, 'bad_data', 0, 100],
        'vote_average': [7.5, 8.0, 6.5, 11.0, -1.0],  # Out of range values
        'release_date': ['2020-01-01', '2060-06-15', '2021-03-20', '1850-01-01', 'invalid'],  # Future and old dates
        'director': ['Director A', 'Director B', None, 'Director D', 'Director E'],
        'cast': ['Actor A|Actor B', 'Actor C', '', 'Actor D', None],
        'genres': ['Action|Drama', 'Comedy', 'Horror', None, 'Sci-Fi']
    })
