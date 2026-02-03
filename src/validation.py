"""Data validation and quality checking module"""
import pandas as pd
import logging
from typing import Dict, List, Any, Optional
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class DataQualityReport:
    """
    Data quality metrics and validation results
    
    Performs comprehensive data quality checks and generates reports
    without silently coercing values.
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize quality report
        
        Args:
            df: DataFrame to validate
        """
        self.df = df
        self.issues: List[str] = []
        self.metrics: Dict[str, Any] = {}
    
    def validate_schema(self, expected_columns: List[str]) -> bool:
        """
        Validate required columns exist
        
        Args:
            expected_columns: List of required column names
            
        Returns:
            True if all columns exist, False otherwise
        """
        missing = set(expected_columns) - set(self.df.columns)
        if missing:
            msg = f"Missing required columns: {missing}"
            self.issues.append(msg)
            logger.error(msg)
            return False
        
        logger.info(f"Schema validation passed: {len(expected_columns)} required columns found")
        return True
    
    def check_missing_values(self, threshold: float = 0.5) -> Dict[str, float]:
        """
        Report missing values, warn if > threshold
        
        Args:
            threshold: Warning threshold for missing percentage (0.0-1.0)
            
        Returns:
            Dictionary of column: missing_percentage
        """
        missing_pct = (self.df.isnull().sum() / len(self.df))
        critical = missing_pct[missing_pct > threshold]
        
        if not critical.empty:
            for col, pct in critical.items():
                msg = f"Column '{col}' has {pct:.1%} missing values (threshold: {threshold:.1%})"
                self.issues.append(msg)
                logger.warning(msg)
        
        # Log summary
        total_missing = missing_pct[missing_pct > 0]
        if not total_missing.empty:
            logger.info(f"Missing values found in {len(total_missing)} columns")
        
        self.metrics['missing_values'] = missing_pct.to_dict()
        return missing_pct.to_dict()
    
    def check_duplicates(self) -> int:
        """
        Report duplicate rows (but don't remove them)
        
        Note: Duplicates are kept to match reference values,
        tracked separately in data_issues.json
        
        Returns:
            Number of duplicate rows
        """
        dup_mask = self.df.duplicated()
        dup_count = dup_mask.sum()
        
        if dup_count > 0:
            msg = f"Found {dup_count} duplicate rows ({dup_count/len(self.df):.1%} of data)"
            self.issues.append(msg)
            logger.info(f"{msg} - keeping for reference match")
        else:
            logger.info("No duplicate rows found")
        
        self.metrics['duplicates'] = int(dup_count)
        return int(dup_count)
    
    def check_data_types(self, numeric_cols: List[str]) -> Dict[str, int]:
        """
        Check and report type coercion issues
        
        IMPORTANT: This reports values that would be coerced to NaN,
        making data quality issues visible instead of silent.
        
        Args:
            numeric_cols: List of columns that should be numeric
            
        Returns:
            Dictionary of column: count_of_coerced_values
        """
        coercion_report = {}
        
        for col in numeric_cols:
            if col not in self.df.columns:
                logger.warning(f"Column '{col}' not found in dataframe")
                continue
            
            # Count non-null values before conversion
            before = self.df[col].notna().sum()
            
            # Try conversion
            converted = pd.to_numeric(self.df[col], errors='coerce')
            
            # Count non-null values after conversion
            after = converted.notna().sum()
            coerced = before - after
            
            if coerced > 0:
                msg = f"Column '{col}': {coerced} values would be coerced to NaN during numeric conversion"
                self.issues.append(msg)
                logger.warning(msg)
                coercion_report[col] = coerced
                
                # Log sample of problematic values
                problematic = self.df[col][pd.to_numeric(self.df[col], errors='coerce').isna() & self.df[col].notna()]
                if len(problematic) > 0:
                    sample = problematic.head(3).tolist()
                    logger.warning(f"  Sample problematic values in '{col}': {sample}")
        
        if not coercion_report:
            logger.info(f"All numeric columns converted successfully without coercion")
        
        self.metrics['type_coercion'] = coercion_report
        return coercion_report
    
    def check_date_range(self, date_col: str, min_year: int = 1900, max_year: int = 2026) -> Dict[str, int]:
        """
        Check for dates outside expected range
        
        Args:
            date_col: Name of date column
            min_year: Minimum valid year
            max_year: Maximum valid year
            
        Returns:
            Dictionary with counts of out-of-range dates
        """
        if date_col not in self.df.columns:
            logger.warning(f"Date column '{date_col}' not found")
            return {}
        
        # Convert to datetime if not already
        dates = pd.to_datetime(self.df[date_col], errors='coerce')
        
        # Check range
        too_old = (dates.dt.year < min_year).sum()
        too_new = (dates.dt.year > max_year).sum()
        
        if too_old > 0:
            msg = f"Found {too_old} dates before {min_year}"
            self.issues.append(msg)
            logger.warning(msg)
        
        if too_new > 0:
            msg = f"Found {too_new} dates after {max_year} (likely 2-digit year parsing errors)"
            self.issues.append(msg)
            logger.warning(msg)
        
        result = {'before_min': too_old, 'after_max': too_new}
        self.metrics['date_range'] = result
        return result
    
    def check_negative_values(self, columns: List[str]) -> Dict[str, int]:
        """
        Check for negative values in columns that should be positive
        
        Args:
            columns: List of column names to check
            
        Returns:
            Dictionary of column: count_of_negative_values
        """
        negative_report = {}
        
        for col in columns:
            if col not in self.df.columns:
                continue
            
            # Convert to numeric first
            values = pd.to_numeric(self.df[col], errors='coerce')
            negative_count = (values < 0).sum()
            
            if negative_count > 0:
                msg = f"Column '{col}' has {negative_count} negative values"
                self.issues.append(msg)
                logger.warning(msg)
                negative_report[col] = negative_count
        
        self.metrics['negative_values'] = negative_report
        return negative_report
    
    def generate_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive quality report
        
        Returns:
            Dictionary with all quality metrics and issues
        """
        report = {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'issues_count': len(self.issues),
            'issues': self.issues,
            'metrics': self.metrics
        }
        
        logger.info(f"Data quality report generated: {len(self.issues)} issues found")
        return report
    
    def save_report(self, output_path: Optional[str] = None) -> None:
        """
        Save quality report to JSON file
        
        Args:
            output_path: Path to save report (default: outputs/data_quality_report.json)
        """
        if output_path is None:
            output_path = Path("outputs") / "data_quality_report.json"
        else:
            output_path = Path(output_path)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        report = self.generate_report()
        
        # Convert numpy types to Python types for JSON serialization
        def convert_types(obj):
            """Convert numpy types to Python types"""
            import numpy as np
            if isinstance(obj, dict):
                return {k: convert_types(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_types(item) for item in obj]
            elif isinstance(obj, (np.integer, np.int64)):
                return int(obj)
            elif isinstance(obj, (np.floating, np.float64)):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            else:
                return obj
        
        report = convert_types(report)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Quality report saved to: {output_path}")


def validate_dataframe(df: pd.DataFrame, required_columns: List[str]) -> None:
    """
    Quick validation that raises exception if critical issues found
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        
    Raises:
        ValueError: If validation fails
    """
    if df.empty:
        raise ValueError("DataFrame is empty - no data to process")
    
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    logger.info(f"Quick validation passed: {len(df)} rows, {len(df.columns)} columns")
