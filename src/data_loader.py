import pandas as pd
from typing import Optional
import logging
from reader import MetricsReader

class MetricsDataLoader:
    def __init__(self, data_dir: str = None):
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Data directory: {data_dir}")
        self.reader = MetricsReader(data_dir)
        

    def load_metrics_to_dataframe(self) -> Optional[pd.DataFrame]:
        """Load all metrics files into a pandas DataFrame"""
        try:
            # Get all JSON files sorted by name
            data_files = sorted(self.reader.data_dir.glob("*.json"))
            if not data_files:
                self.logger.warning("No JSON files found in directory")
                return None

            # Load all metrics data
        
            all_metrics = []
            for file in data_files:
                self.logger.info(f"Processing file: {file}")
                metrics = self.reader.get_metrics_from_file(file.name)
                if metrics:
                    all_metrics.extend(metrics)

            if not all_metrics:
                return None

            # Convert to DataFrame
            data = [{
                'date': m.day,
                'suggestions': m.total_suggestions_count,
                'active_users': m.total_active_users,
                'lines_accepted': m.total_lines_accepted  
            } for m in all_metrics]

            return pd.DataFrame(data)

        except Exception as e:
            self.logger.error(f"Error loading metrics data: {str(e)}")
            return None

if __name__ == "__main__":
    # Example usage
    loader = MetricsDataLoader(data_dir="./data")
    
    df = loader.load_metrics_to_dataframe()
    if df is not None:
        print(df.head())
        print(f"\nTotal records: {len(df)}")
    else:
        print("Failed to load metrics data")