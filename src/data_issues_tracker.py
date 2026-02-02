"""Data issues tracker - saves all bad data to single JSON file"""
import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class DataIssuesTracker:
    """
    Track all data issues in a single JSON file
    Chỉ lưu original values (data gốc bị vấn đề)
    """
    
    def __init__(self):
        self.issues: Dict[str, List[Dict[str, Any]]] = {
            'future_dates': [],
            'coerced_values': [],
            'duplicates': []
        }
    
    def add_future_dates(self, df: pd.DataFrame, mask: pd.Series) -> None:
        """Lưu dates bị parse sai"""
        if mask.sum() > 0:
            affected = df.loc[mask, ['id', 'original_title', 'release_date']].copy()
            for _, row in affected.iterrows():
                self.issues['future_dates'].append({
                    'id': int(row['id']),
                    'title': row['original_title'],
                    'original_date': str(row['release_date'])
                })
            logger.info(f"Tracked {len(affected)} future dates")
    
    def add_coerced_values(self, df: pd.DataFrame, col: str, original_values: pd.Series, mask: pd.Series) -> None:
        """Lưu values bị coerce to NaN"""
        if mask.sum() > 0:
            affected = df.loc[mask, ['id', 'original_title']].copy()
            affected['original_value'] = original_values[mask]
            
            for _, row in affected.iterrows():
                self.issues['coerced_values'].append({
                    'id': int(row['id']),
                    'title': row['original_title'],
                    'column': col,
                    'original_value': str(row['original_value'])
                })
            logger.info(f"Tracked {len(affected)} coerced values in column '{col}'")
    
    def add_duplicates(self, df: pd.DataFrame, mask: pd.Series) -> None:
        """Lưu duplicate rows"""
        if mask.sum() > 0:
            affected = df.loc[mask, ['id', 'original_title']].copy()
            for _, row in affected.iterrows():
                self.issues['duplicates'].append({
                    'id': int(row['id']),
                    'title': row['original_title']
                })
            logger.info(f"Tracked {len(affected)} duplicates")
    
    def save(self, output_path: str = None) -> None:
        """Lưu tất cả issues vào 1 file JSON"""
        if output_path is None:
            output_path = Path("outputs") / "data_issues.json"
        else:
            output_path = Path(output_path)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Summary
        summary = {
            'total_issues': sum(len(v) for v in self.issues.values()),
            'future_dates_count': len(self.issues['future_dates']),
            'coerced_values_count': len(self.issues['coerced_values']),
            'duplicates_count': len(self.issues['duplicates'])
        }
        
        output = {
            'summary': summary,
            'issues': self.issues
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Data issues saved to: {output_path}")
        logger.info(f"  Total issues: {summary['total_issues']}")
        logger.info(f"  - Future dates: {summary['future_dates_count']}")
        logger.info(f"  - Coerced values: {summary['coerced_values_count']}")
        logger.info(f"  - Duplicates: {summary['duplicates_count']}")
