# utils.py
import os
import sqlite3

def sanitize_directory_name(dir_name):
    forbidden_chars = ["<", ">", ":", '"', "|", "?", "*"]
    for char in forbidden_chars:
        dir_name = dir_name.replace(char, "")
    return dir_name

def find_or_create_folder(path, folder_name):
    folder_name = sanitize_directory_name(folder_name)
    for root, dirs, _ in os.walk(path):
        if folder_name in dirs:
            return os.path.join(root, folder_name)

    new_folder_path = os.path.join(path, folder_name)
    os.mkdir(new_folder_path)
    return new_folder_path

class DatabaseHandler:
    def __init__(self, db_name="file_links.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    directory_name TEXT,
                    file_name TEXT,
                    file_url TEXT UNIQUE
                );
                """
            )

    def insert_entry(self, directory_name, file_name, file_url):
        with self.conn:
            try:
                self.conn.execute(
                    """
                    INSERT INTO files (directory_name, file_name, file_url)
                    VALUES (?, ?, ?);
                    """,
                    (directory_name, file_name, file_url),
                )
            except sqlite3.IntegrityError:
                pass

    def fetch_entries(self):
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM files;")
            return cursor.fetchall()

    def close(self):
        self.conn.close()

def check_variables(*variables):
    for var in variables:
        if not var:
            raise ValueError(f"Variable '{var}' is empty or has no content.")
