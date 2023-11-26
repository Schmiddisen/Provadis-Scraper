"""Main file for the project. This file will run the scraper and download the files."""
import sys
import traceback
from scraper import scrape_coach, EmptyVariableException
from download_files import download

amount_of_files = 1500
headless = True

if len(sys.argv) > 1:
    amount_of_files = sys.argv[1]
    headless =  sys.argv[2]

if __name__ == "__main__":
    try:
        scrape_coach(amount_of_files=amount_of_files, headless=headless)
        continue_download = True
    except EmptyVariableException as e:
        traceback.print_exc()
        print("[i] A possible fix might be deleting 'file_links.db'.")
        continue_download = False
    except Exception as e:
        print("[!] A fatal error occured while scraping the provadis coach!")
        print("[!] If this issue persists, consider reporting it.")
        traceback.print_exc()
        continue_download = True
    if continue_download:
        try:
            download()
        except Exception as e:
            print("[!] A fatal error occured while downloading the files!")
            print("[!] If this issue persists, consider reporting it.")
            traceback.print_exc()

    input("[i] Press return to close this window.")