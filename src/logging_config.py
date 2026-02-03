"""Logging configuration for TMDB Movie Analysis"""
import logging
from pathlib import Path
from typing import Optional


def setup_logging(
    log_file: str = "tmdb_analysis.log", 
    level: int = logging.INFO
) -> logging.Logger:
    """
    Setup structured logging with file and console handlers
    
    Args:
        log_file: Name of log file to create in outputs/logs/
        level: Logging level (default: INFO)
    
    Returns:
        Configured logger instance
    """
    # Create logs directory
    log_path = Path("outputs") / "logs" / log_file
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path, encoding='utf-8'),
            logging.StreamHandler()
        ],
        force=True  # Override any existing configuration
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_path}")
    
    return logger
