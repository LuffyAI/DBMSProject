## Author: Larnell Moore
## Date: April 3, 2024
## Purpose: Creates a sample database for the Backend using default values and stores it in the DatabaseManager.
## Run this file if you want to reset the database to its default values.

import sqlite3
import os

files = ['sql/tables.sql', 'sql/triggers.sql', 'sql/insertions.sql']

def execute_sql_file(cursor, filepath):
        with open(filepath, 'r') as file:
            sql_script = file.read()
        cursor.executescript(sql_script)

def initDatabase(db_path, files_to_execute):
    # Check if the database already exists and remove it
    if os.path.exists(db_path):
        os.remove(db_path)

    # Connect to SQLite (this will create a new database)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Enable foreign key constraint enforcement
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Execute SQL files in the required order
    for file in files_to_execute:
        execute_sql_file(cursor, file)
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    initDatabase('DatabaseManager/RecallDatabase.db', files)
