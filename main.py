"""Main file for the project. This file will run the scraper and download the files."""
import os
from scraper import scrape_coach
from download_files import download


if __name__ == "__main__":
    scrape_coach(amount_of_files=1500, headless=False)
    download()
