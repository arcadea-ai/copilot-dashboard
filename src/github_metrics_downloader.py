import os
import json
import logging
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv('.env')

class GithubMetricsDownloader:
    def __init__(self):
        self.api_key = str(os.getenv("GITHUB_API_KEY"))
        self.org = str(os.getenv("GITHUB_ORG_NAME"))
        self.api_version = str(os.getenv("GITHUB_API_VERSION", "2022-11-28"))
        self.endpoint = f"https://api.github.com/orgs/{self.org}/copilot/metrics"
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.api_key}",
            "X-GitHub-Api-Version": self.api_version
        }
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self._setup_logging()
    
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def process_data(self, raw_data):
        processed_data = []
        for entry in raw_data:
            try:
                x = entry["date"]
            except Exception:
                print("Error: ", entry)
                continue
            processed_entry = {
                "day": entry["date"],
                "total_suggestions_count": 0,
                "total_acceptances_count": 0,
                "total_lines_suggested": 0,
                "total_lines_accepted": 0,
                "total_active_users": entry.get("total_active_users", 0),
                "total_chat_acceptances": 0,
                "total_chat_turns": 0,
                "total_active_chat_users": 0
            }
            
            if "copilot_ide_code_completions" in entry:
                for editor in entry["copilot_ide_code_completions"].get("editors", []):
                    for model in editor.get("models", []):
                        for language in model.get("languages", []):
                            processed_entry["total_suggestions_count"] += language.get("total_code_suggestions", 0)
                            processed_entry["total_acceptances_count"] += language.get("total_code_acceptances", 0)
                            processed_entry["total_lines_suggested"] += language.get("total_code_lines_suggested", 0)
                            processed_entry["total_lines_accepted"] += language.get("total_code_lines_accepted", 0)
            
            if "copilot_ide_chat" in entry:
                for editor in entry["copilot_ide_chat"].get("editors", []):
                    for model in editor.get("models", []):
                        processed_entry["total_chat_turns"] += model.get("total_chats", 0)
                        processed_entry["total_chat_acceptances"] += model.get("total_chat_insertion_events", 0) + model.get("total_chat_copy_events", 0)
                        processed_entry["total_active_chat_users"] += model.get("total_engaged_users", 0)
            
            processed_data.append(processed_entry)
        
        return processed_data
    
    def download(self):
        try:
            response = requests.get(self.endpoint, headers=self.headers)
            
            if response.status_code != 200:
                logging.error(f"Failed to fetch data: {response.status_code} - {response.text}")
                return None
            
            raw_data = response.json()
            processed_data = self.process_data(raw_data)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.data_dir / f"metrics_{timestamp}.json"
            
            with open(output_file, 'w') as f:
                json.dump(processed_data, f, indent=2)
            
            logging.info(f"Data saved to {output_file}")
            return output_file
        
        except requests.RequestException as e:
            logging.error(f"Error fetching data: {e}")
            return None

if __name__ == "__main__":
    downloader = GithubMetricsDownloader()
    downloader.download()
