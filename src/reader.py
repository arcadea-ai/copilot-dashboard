"""
This module provides functionality to read and parse daily metrics from JSON files.
"""

from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import json
import logging

@dataclass
class DailyMetrics:
    """
    Stores daily metrics.
    """
    day: datetime
    total_suggestions_count: int
    total_acceptances_count: int
    total_lines_suggested: int
    total_lines_accepted: int
    total_active_users: int
    total_chat_acceptances: int
    total_chat_turns: int
    total_active_chat_users: int

class MetricsReader:
    """
    Reads and parses metrics from JSON files.
    """
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the MetricsReader with the directory containing data files.
        """
        self.data_dir = Path(data_dir)
        self._setup_logging()

    def _setup_logging(self):
        """
        Setup logging configuration.
        """
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def read_metrics_file(self, filename: str) -> Optional[List[DailyMetrics]]:
        """
        Read and parse a metrics file.

        Args:
            filename (str): The name of the file to read.

        Returns:
            Optional[List[DailyMetrics]]: A list of DailyMetrics objects or None if an error occurs.
        """
        try:
            file_path = self.data_dir / filename
            with open(file_path) as f:
                data = json.load(f)
            
            return [self._parse_daily_metrics(item) for item in data]
        except Exception as e:
            logging.error(f"Error reading metrics file {filename}: {str(e)}")
            return None

    def _parse_daily_metrics(self, data: Dict) -> DailyMetrics:
        """
        Parse a dictionary into a DailyMetrics object.

        Args:
            data (Dict): The dictionary containing daily metrics data.

        Returns:
            DailyMetrics: The parsed DailyMetrics object.
        """
        return DailyMetrics(
            day=datetime.strptime(data["day"], "%Y-%m-%d"),
            total_suggestions_count=data["total_suggestions_count"],
            total_acceptances_count=data["total_acceptances_count"],
            total_lines_suggested=data["total_lines_suggested"],
            total_lines_accepted=data["total_lines_accepted"],
            total_active_users=data["total_active_users"],
            total_chat_acceptances=data["total_chat_acceptances"],
            total_chat_turns=data["total_chat_turns"],
            total_active_chat_users=data["total_active_chat_users"]
        )

    def get_metrics_from_file(self, filename: str) -> Optional[List[DailyMetrics]]:
        """
        Get metrics from a specified file.

        Args:
            filename (str): The name of the file to read.

        Returns:
            Optional[List[DailyMetrics]]: A list of DailyMetrics objects or None if an error occurs.
        """
        try:
            return self.read_metrics_file(filename)
        except Exception as e:
            logging.error(f"Error getting metrics from file {filename}: {str(e)}")
            return None

if __name__ == "__main__":
    reader = MetricsReader()
    data_files = sorted(reader.data_dir.glob("*.json"))
    if data_files:
        latest_file = data_files[0]
        metrics = reader.get_metrics_from_file(latest_file.name)
        if metrics:
            for daily in metrics:
                print(f"Date: {daily.day.strftime('%Y-%m-%d')}")
                print(f"Total suggestions: {daily.total_suggestions_count}")
                print(f"Active users: {daily.total_active_users}")
    else:
        print("No data files found.")

        