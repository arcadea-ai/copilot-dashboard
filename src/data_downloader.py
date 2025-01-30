#!/usr/bin/env python3
import logging
import sys
import os
import streamlit as st

from github_metrics_downloader import GithubMetricsDownloader
from data_manager import DataManager


def setup_logging():
    """Setup logging to console"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )

@st.cache_data(ttl=43200)  # Cache expires after 12 hours (43200 seconds)
def data_downloader():
    setup_logging()
    logger = logging.getLogger('DataDownloader')
    
    try:
        # Download latest metrics
        logger.info("Starting download of GitHub metrics...")
        downloader = GithubMetricsDownloader()
        downloaded_file = downloader.download()
        logger.info(f"Downloaded file: {downloaded_file.name}")
        
        if not downloaded_file:
            logger.error("Failed to download metrics. Check GitHub API token and Storage permissions.")
            return 1
            
        # Process and save data
        logger.info(f"Processing downloaded file: {downloaded_file}")
        manager = DataManager()
        result = manager.process_new_data(downloaded_file.name)
        
        if result:
            logger.info(f"Successfully processed and saved data to: {result}")
        else:
            logger.info("No new data to save.")
            return 1
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return 1
    
    finally:
        # Ensure the temporary file is deleted
        if downloaded_file:
            os.remove(str(downloaded_file))
            logger.info(f"Deleted temporary file: {str(downloaded_file)}")

if __name__ == "__main__":
    data_downloader()