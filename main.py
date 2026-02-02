"""Main entry point for TMDB Movie Analysis"""
import sys
import argparse
import logging

from src.config import DATA_URL, validate_config
from src.logging_config import setup_logging
from src.etl import load_data, clean_data, profile_data

# Import task modules
from src.tasks import (
    task1_sorting, task2_filtering, task3_revenue, task4_total,
    task5_profit, task6_talent, task7_genres, task8_roi
)

logger = logging.getLogger(__name__)


def main():
    """Main execution function"""
    
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description="TMDB Movie Analysis - Data Engineering Project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Run all tasks
  python main.py --task 5           # Run task 5 only
  python main.py --plot             # Run all tasks with visualizations
  python main.py --task 1 --plot    # Run task 1 with visualization
        """
    )
    
    parser.add_argument(
        '--url', 
        type=str, 
        default=DATA_URL, 
        help='Data source URL (default: TMDB movies dataset)'
    )
    
    parser.add_argument(
        '--task', 
        type=int, 
        choices=range(1, 9), 
        help='Run specific task number (1-8)'
    )
    
    parser.add_argument(
        '--plot', 
        action='store_true', 
        help='Generate visualization charts'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    setup_logging(level=log_level)
    
    logger.info("=" * 70)
    logger.info("TMDB MOVIE ANALYSIS - DATA ENGINEERING PROJECT")
    logger.info("=" * 70)
    
    # Validate configuration
    try:
        validate_config()
        logger.info("Configuration validated successfully")
    except ValueError as e:
        logger.error(f"Configuration validation failed: {e}")
        sys.exit(1)
    
    # Load and clean data
    logger.info(f"Data source: {args.url}")
    
    try:
        # ETL Pipeline
        raw_df = load_data(args.url)
        df_clean = clean_data(raw_df)
        
        # Data profiling
        profile_data(df_clean)
        
    except Exception as e:
        logger.error(f"ETL Pipeline failed: {e}", exc_info=True)
        sys.exit(1)
    
    # Task dispatcher
    task_map = {
        1: task1_sorting,
        2: task2_filtering,
        3: task3_revenue,
        4: task4_total,
        5: task5_profit,
        6: task6_talent,
        7: task7_genres,
        8: task8_roi
    }
    
    # Execute tasks
    task_id = args.task
    
    if task_id:
        # Run specific task
        logger.info(f"Running Task {task_id}...")
        try:
            task_map[task_id].run(df_clean, plot=args.plot)
        except Exception as e:
            logger.error(f"Task {task_id} failed: {e}", exc_info=True)
            sys.exit(1)
    else:
        # Run all tasks
        logger.info("Running ALL tasks...")
        failed_tasks = []
        
        for t_id, module in task_map.items():
            try:
                logger.info(f"\n{'='*60}")
                module.run(df_clean, plot=args.plot)
                logger.info(f"{'='*60}")
            except Exception as e:
                logger.error(f"Task {t_id} failed: {e}", exc_info=True)
                failed_tasks.append(t_id)
        
        if failed_tasks:
            logger.error(f"Failed tasks: {failed_tasks}")
            sys.exit(1)
    
    logger.info("\n" + "=" * 70)
    logger.info("ANALYSIS COMPLETE")
    logger.info("=" * 70)
    logger.info("Check outputs/ directory for results:")
    logger.info("  - CSV files (sorted_by_date.csv, high_rated_movies.csv)")
    logger.info("  - Visualizations (outputs/plots/)")
    logger.info("  - Logs (outputs/logs/tmdb_analysis.log)")
    logger.info("  - Data quality report (outputs/data_quality_report.json)")


if __name__ == "__main__":
    main()

