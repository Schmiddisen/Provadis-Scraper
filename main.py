# main.py
import sys
import traceback
from scraper import scrape_coach
from download_files import download

def main():
    amount_of_files = 1500
    headless = True
    browser = "firefox"

    if len(sys.argv) > 1:
        amount_of_files = int(sys.argv[1])
    if len(sys.argv) > 2:
        headless = sys.argv[2].lower() in ['true', '1', 't', 'y', 'yes']
    if len(sys.argv) > 3:
        browser = sys.argv[3].lower()

    try:
        scrape_coach(amount_of_files=amount_of_files, headless=headless, browser=browser)
        continue_download = True
    except Exception as e:
        print("[!] A fatal error occurred while scraping the provadis coach!")
        print("[!] If this issue persists, consider reporting it.")
        traceback.print_exc()
        continue_download = False

    if continue_download:
        try:
            download()
        except Exception as e:
            print("[!] A fatal error occurred while downloading the files!")
            print("[!] If this issue persists, consider reporting it.")
            traceback.print_exc()

if __name__ == "__main__":
    main()
