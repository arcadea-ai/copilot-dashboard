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
        self.endpoint = f"https://api.github.com/orgs/{self.org}/copilot/usage"
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
    
    def download(self):
        try:
            response = requests.get(self.endpoint, headers=self.headers)
            
            if response.status_code != 200:
                logging.error(f"Failed to fetch data: {response.status_code} - {response.text}")
                return None
            
            data = response.json()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.data_dir / f"metrics_{timestamp}.json"
            
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logging.info(f"Data saved to {output_file}")
            return output_file
        
        except requests.RequestException as e:
            logging.error(f"Error fetching data: {e}")
            return None

if __name__ == "__main__":
    downloader = GithubMetricsDownloader()
    downloader.download()
