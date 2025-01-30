from pathlib import Path
import json
import logging
from datetime import datetime
from typing import Optional, List
import re
from reader import MetricsReader, DailyMetrics

class DataManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.reader = MetricsReader(data_dir)
        self._setup_logging()

    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def _find_latest_data_file(self) -> Optional[Path]:
        data_files = list(self.data_dir.glob("data_*.json"))
        if not data_files:
            return None
        
        # Extract dates from filenames and find latest
        date_pattern = re.compile(r'data_(\d{4}-\d{2}-\d{2})\.json')
        dated_files = []
        for file in data_files:
            match = date_pattern.match(file.name)
            if match:
                date_str = match.group(1)
                dated_files.append((datetime.strptime(date_str, "%Y-%m-%d"), file))
        
        return max(dated_files, key=lambda x: x[0])[1] if dated_files else None

    def _get_existing_dates(self, file_path: Path) -> set:
        try:
            metrics = self.reader.read_metrics_file(file_path.name)
            if metrics:
                return {m.day for m in metrics}
            return set()
        except Exception:
            return set()

    def _save_metrics(self, metrics: List[DailyMetrics], output_path: Path) -> None:
        metrics_json = [
            {
                "day": m.day.strftime("%Y-%m-%d"),
                "total_suggestions_count": m.total_suggestions_count,
                "total_acceptances_count": m.total_acceptances_count,
                "total_lines_suggested": m.total_lines_suggested,
                "total_lines_accepted": m.total_lines_accepted,
                "total_active_users": m.total_active_users,
                "total_chat_acceptances": m.total_chat_acceptances,
                "total_chat_turns": m.total_chat_turns,
                "total_active_chat_users": m.total_active_chat_users
            }
            for m in metrics
        ]

        with open(output_path, 'w') as f:
            json.dump(metrics_json, f, indent=2)

        logging.info(f"Saved {len(metrics)} new metrics to {output_path.name}")

    def process_new_data(self, input_file: str) -> Optional[str]:
        try:
            # Read new data
            new_metrics = self.reader.read_metrics_file(input_file)
            if not new_metrics:
                logging.error("No data found in input file")
                return None

            # Find latest existing data file
            latest_file = self._find_latest_data_file()
            latest_day = None
            if latest_file:
                logging.info(f"Latest data file found: {latest_file.name}")
                existing_dates = self._get_existing_dates(latest_file)
                if existing_dates:
                    latest_day = max(existing_dates)
                    logging.info(f"Latest day in existing data: {latest_day.strftime('%Y-%m-%d')}")

            # Filter out dates before or on the latest day
            if latest_day:
                unique_metrics = [m for m in new_metrics if m.day > latest_day]
            else:
                unique_metrics = new_metrics

            if not unique_metrics:
                logging.info("No new metrics to save")
                return None

            # Find last day for filename
            last_day = max(m.day for m in unique_metrics)
            logging.info(f"Last day in new metrics: {last_day.strftime('%Y-%m-%d')}")
            output_filename = f"data_{last_day.strftime('%Y-%m-%d')}.json"
            output_path = self.data_dir / output_filename

            # Save new data
            self._save_metrics(unique_metrics, output_path)
            return output_filename

        except Exception as e:
            logging.error(f"Error processing new data: {str(e)}")
            return None

if __name__ == "__main__":
    manager = DataManager()
    # Example usage with a downloaded metrics file
    result = manager.process_new_data("metrics_20241101_220634.json")
    if result:
        print(f"Processed and saved to: {result}")
