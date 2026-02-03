import sys
import argparse
from src.config import DATA_URL
from src.etl import load_data, clean_data

# Import task modules
from src.tasks import (
    task1_sorting, task2_filtering, task3_revenue, task4_total,
    task5_profit, task6_talent, task7_genres, task8_roi
)

def main():
    parser = argparse.ArgumentParser(description="TMDB Movie Analysis Project")
    parser.add_argument('--url', type=str, default=DATA_URL, help='Data source URL')
    parser.add_argument('--local', type=str, help='Local file path (overrides URL)')
    parser.add_argument('--task', type=int, choices=range(1, 9), help='Run specific task number (1-8)')
    parser.add_argument('--plot', action='store_true', help='Generate charts')
    args = parser.parse_args()

    # Determine source and load data
    source = args.local if args.local else args.url
    print(f"Starting analysis from: {source}")
    try:
        raw_df = load_data(source)
        df_clean = clean_data(raw_df)
    except Exception as e:
        print(f"ETL Failed: {e}")
        sys.exit(1)

    # Task Dispatcher
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

    # Execute
    task_id = args.task
    
    if task_id:
        # Run specific task
        if task_id in task_map:
            task_map[task_id].run(df_clean, plot=args.plot)
        else:
            print(f"Task {task_id} not implemented.")
    else:
        # Run all tasks (Optional: Could disable plot for all run to avoid spam, or keep it)
        print("Running ALL Tasks...")
        for t_id, module in task_map.items():
            try:
                module.run(df_clean, plot=args.plot)
            except Exception as e:
                print(f"Error running Task {t_id}: {e}")
            print("-" * 40)

if __name__ == "__main__":
    main()
