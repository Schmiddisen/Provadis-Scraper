import time
import main

sleeptime_in_minutes = 10

def scrape_coach():
    while True:
        main.main()  # Aufruf der main Funktion des Projekts
        time.sleep(sleeptime_in_minutes * 60)

if __name__ == "__main__":
    scrape_coach()
