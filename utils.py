"""This file contains utility methods and classes."""
import os
import sqlite3


def sanitize_directory_name(dir_name):
    """
    This method removes forbidden characters from a directory name.
    """
    forbidden_chars = ["<", ">", ":", '"', "|", "?", "*"]
    for char in forbidden_chars:
        dir_name = dir_name.replace(char, "")
    return dir_name


def find_or_create_folder(path, folder_name):
    """
    This method searches for a folder in the given path and creates it if it doesn't exist yet.
    """
    folder_name = sanitize_directory_name(folder_name)
    # search for folder in path and return path if found
    for root, dirs, _ in os.walk(path):
        if folder_name in dirs:
            return os.path.join(root, folder_name)

    # create folder if not found
    new_folder_path = os.path.join(path, folder_name)
    os.mkdir(new_folder_path)
    return new_folder_path


class DatabaseHandler:
    """
    This class handles the database connection and provides methods to insert and fetch entries.
    """
    def __init__(self, db_name="file_links.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        """
        This method creates the table if it doesn't exist yet.
        """
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
        """
        This method inserts an entry into the database.
        """
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
        """
        This method fetches all entries from the database.
        """
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM files;")
            return cursor.fetchall()

    def close(self):
        """
        This method closes the connection to the database.
        """
        self.conn.close()
