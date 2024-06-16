# scraper.py
import json
import os
from time import sleep
from dotenv import load_dotenv
from msedge.selenium_tools import Edge, EdgeOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import *
from utils import DatabaseHandler

load_dotenv()
LOGIN_URL = "https://hochschule.provadis-coach.de/view.php?view=files"
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
db_handler = DatabaseHandler()

def login_process_microsoft(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.ID, "i0116"))).send_keys(EMAIL)
    wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
    wait.until(EC.element_to_be_clickable((By.NAME, "passwd"))).send_keys(PASSWORD)

    for _ in range(3):  # Retry login a few times if needed
        try:
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-report-event='Signin_Submit']"))).click()
            break
        except StaleElementReferenceException:
            sleep(1)

    wait.until(EC.element_to_be_clickable((By.ID, "idBtn_Back"))).click()

def set_files_per_page(driver, amount_of_files):
    wait = WebDriverWait(driver, 50)
    if amount_of_files == 0:
        return

    select_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'select[name="files_table_length"]')))
    driver.execute_script(f"arguments[0].add(new Option({amount_of_files}, {amount_of_files}));", select_element)
    select = Select(select_element)
    select.select_by_value(str(amount_of_files))
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr[class='odd'], tr[class='even']")))

def get_table_rows(driver):
    wait = WebDriverWait(driver, 10)
    for _ in range(5):
        try:
            table_rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr[class='odd'], tr[class='even']")))
            return table_rows
        except StaleElementReferenceException:
            continue

    raise Exception("Unable to retrieve table rows after multiple attempts")

def process_table_rows(table_rows, db_handler, driver):
    try:
        for row in table_rows:
            file_link = row.find_element(By.CSS_SELECTOR, "td > a")
            file_url = file_link.get_attribute("href")
            directory_name = row.find_element(By.XPATH, './td[last()]').text
            file_name = file_link.text
            if not all([file_link, file_url, directory_name, file_name]):
                raise ValueError("One or more variables are empty or have no content.")
            db_handler.insert_entry(directory_name, file_name, file_url)
    except StaleElementReferenceException:
        table_rows_new = get_table_rows(driver)
        process_table_rows(table_rows_new, db_handler, driver)

def scrape_coach(amount_of_files=0, headless=True, browser="edge"):
    print("[i] Beginning scraping process!")
    print(f"[i] Checking the first {amount_of_files} files")

    if browser == "edge":
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument("--inprivate")
        if headless:
            options.add_argument("--headless")
        options.add_argument("--log-level=OFF")
        driver = Edge(options=options, executable_path="./msedgedriver.exe")
    elif browser == "firefox":
        from webdriver_manager.firefox import GeckoDriverManager
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.get(LOGIN_URL)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-lg.btn-default.btn-block"))).click()

    print("[i] logging in")
    login_process_microsoft(driver)

    print("[i] Navigating to file section")
    wait.until(EC.element_to_be_clickable((By.ID, "files"))).click()
    wait.until(EC.element_to_be_clickable((By.ID, "displaymode"))).click()

    set_files_per_page(driver, amount_of_files)

    print("[i] getting file links")
    table_rows = get_table_rows(driver)

    print("[i] writing db entries")
    process_table_rows(table_rows, db_handler, driver)

    cookies = driver.get_cookies()
    with open("cookies.json", "w", encoding="utf-8") as f:
        json.dump(cookies, f)

    driver.quit()
    db_handler.close()
    print("[i] Scraping done!")
