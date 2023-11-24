"""This module contains the scraper for the coach website. It uses selenium to navigate the website 
and save the file links in a database."""
import json
import os
from dotenv import load_dotenv
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import *
from utils import DatabaseHandler

# Load environment variables
load_dotenv()
password = os.getenv("PASSWORD")
email = os.getenv("EMAIL")
 
# Initialize Database
db_handler = DatabaseHandler()

def click_login_button(driver: Edge):
    """
    This method clicks the login button. It is needed because the button is sometimes not found.
    """
    login_submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-report-event='Signin_Submit']"))
    )
    login_submit_button.click()


def login_process_microsoft(driver: Edge):
    """
    This method handles the login process for the microsoft login page.
    """
    wait = WebDriverWait(driver, 10)
    email_elem =wait.until(
        EC.element_to_be_clickable((By.ID, "i0116"))
    )
    print("[i] Sending email")
    email_elem.send_keys(email)

    send_button = driver.find_element(By.ID, "idSIButton9")
    send_button.click()
    print("[i] Navigating to password page")

    password_elem =wait.until(
        EC.element_to_be_clickable((By.NAME, "passwd"))
    )
    print("[i] Sending password")
    password_elem.send_keys(password)

    print("[i] Clicking login button")
    try:
        click_login_button(driver)
    except StaleElementReferenceException:
        click_login_button(driver)

    # Skip stay signed in
    no_button =wait.until(
        EC.element_to_be_clickable((By.ID, "idBtn_Back"))
    )
    no_button.click()

def set_files_per_page(driver: Edge, amount_of_files):
    wait = WebDriverWait(driver, 50)
    if amount_of_files != 0:
        select_element = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'select[name="files_table_length"]'))
        )

        driver.execute_script(f"arguments[0].add(new Option({amount_of_files}, {amount_of_files}));", select_element)
        select = Select(select_element)
        select.select_by_value(str(amount_of_files))
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr[class='odd'], tr[class='even']")))
    else:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr[class='odd'], tr[class='even']")))

def get_table_rows(driver: Edge):
    wait = WebDriverWait(driver, 10)
    for _ in range(5):  # Retry up to 5 times in case of StaleElementReferenceException
        try:
            table_rows = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr[class='odd'], tr[class='even']"))
            )
            return table_rows
        except StaleElementReferenceException:
            continue  # Retry if a StaleElementReferenceException occurs

    raise Exception("Unable to retrieve table rows after multiple attempts")

def process_table_rows(table_rows, db_handler: DatabaseHandler, driver: Edge):
    try:
        for row in table_rows:
            file_link = row.find_element(By.CSS_SELECTOR, "td > a")
            file_url = file_link.get_attribute("href")
            directory_name = row.find_element(By.XPATH, './td[last()]').text
            file_name = file_link.text
            db_handler.insert_entry(directory_name, file_name, file_url)
        return
    except StaleElementReferenceException:
            table_rows_new = get_table_rows(driver)
            process_table_rows(table_rows_new, db_handler, driver)

def scrape_coach(amount_of_files=0, headless=True):
    """
    This method scrapes the coach website and saves the file links in a database.
    """
    print("[i] Beginning scraping process!")
    print(f"[i] Checking the first {amount_of_files} files")

    # Initialize WebDriver
    edge_options = EdgeOptions()
    edge_options.use_chromium = True
    edge_options.add_argument("--inprivate")
    if headless:
        edge_options.add_argument("--headless")
    driver = Edge(options=edge_options, executable_path="./msedgedriver.exe")

    # Navigate to website
    driver.get("https://hochschule.provadis-coach.de/view.php?view=files")

    wait = WebDriverWait(driver, 10)

    # Start login process
    try:
        login_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-lg.btn-default.btn-block"))
        )
        login_button.click()
    except Exception as e:
        print(f"[!] Error clicking login button: {e}")
        return

    print("[i] logging in")
    login_process_microsoft(driver)

    print("[i] Navigating to file section")
    # Change to file view
    files_button =wait.until(
        EC.element_to_be_clickable((By.ID, "files"))
    )
    files_button.click()

    # Change to list view
    displaymode_button =wait.until(
        EC.element_to_be_clickable((By.ID, "displaymode"))
    )
    displaymode_button.click()

    set_files_per_page(driver, amount_of_files)

    print("[i] getting file links")
    table_rows = get_table_rows(driver)

    print("[i] writing db entries")
    process_table_rows(table_rows, db_handler, driver)

# save cookies for requests
    cookies = driver.get_cookies()

    with open("cookies.json", "w", encoding="utf-8") as f:
        json.dump(cookies, f)
        f.close()

    driver.quit()
    db_handler.close()
    print("[i] Scraping done!")
    