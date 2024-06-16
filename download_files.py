# download_files.py
import os
import json
import requests
from utils import DatabaseHandler, find_or_create_folder

def download():
    try:
        with open("cookies.json", "r", encoding="utf-8") as f:
            cookies = json.load(f)
    except FileNotFoundError:
        print("[!] cookies.json missing")
        return

    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie["name"], cookie["value"])

    db_handler = DatabaseHandler()
    entries = db_handler.fetch_entries()
    db_handler.close()

    path = os.path.join(os.getcwd(), "..", "Provadis-Coach-Mirror")

    for entry in entries:
        directory_name, file_name, file_url = entry[1], entry[2], entry[3]
        folder_path = find_or_create_folder(path, directory_name)
        file_path = os.path.join(folder_path, file_name)

        if os.path.exists(file_path):
            continue

        print(f"[i] found new file: {file_name} in {directory_name}")
        response = s.get(file_url)
        if response.status_code == 200:
            try:
                with open(file_path, "wb") as f:
                    f.write(response.content)
            except FileNotFoundError as e:
                print(f"[!] Error while writing file: {e}")
    print("[i] finished downloading files.")
