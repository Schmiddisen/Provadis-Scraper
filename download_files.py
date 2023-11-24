"""
This module downloads all files from the database. It uses the cookies from the login process to 
authenticate the requests.
"""
import os
import json
import requests
from utils import DatabaseHandler, find_or_create_folder


def download():
    """
    This method downloads all files from the database.
    """
    # Load cookies
    try:
        with open("cookies.json", "r", encoding="utf-8") as f:
            cookies = json.load(f)
    except FileNotFoundError:
        print("[!] cookies.json missing")
        return

    # Initialize Requests session
    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie["name"], cookie["value"])

    # Initialize Database and fetch entries
    db_handler = DatabaseHandler()
    entries = db_handler.fetch_entries()
    db_handler.close()

    # Set save path
    path = os.path.join(os.getcwd(), "..", "Provadis-Coach-Mirror")

    # Download files
    for entry in entries:
        directory_name, file_name, file_url = entry[1], entry[2], entry[3]
        folder_path = find_or_create_folder(path, directory_name)
        # Construct the full file path
        file_path = os.path.join(folder_path, file_name)
        # Check if the file already exists
        if os.path.exists(file_path):
            continue
        # Print if new file is found
        print(f"[i] found new file: {file_name} in {directory_name}")

        # Download file
        response = s.get(file_url)
        if response.status_code == 200:
            try:
                with open(file_path, "wb") as f:
                    f.write(response.content)
            except FileNotFoundError as e:
                print(f"[!] Error while writing file: {e}")
    print("[i] finished downloading files.")
