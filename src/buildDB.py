## Author: Larnell Moore
## Creation Date: Feb 14 2024
## Purpose: Scraps the SQL schemas from the schema folder and builds the tables. 
import sqlite3
import glob
import os

def execute_sql_files_from_folder(db_path, folder_path):
    """Scraps all .sql files from schema and runs them on a specified database file"""
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Find all .sql files in the specified folder
    sql_files = glob.glob(os.path.join(folder_path, '*.sql'))
    
    for sql_file in sql_files:
        print(f"Executing commands from {sql_file}")
        with open(sql_file, 'r') as file:
            sql_script = file.read()
            cursor.executescript(sql_script)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("All SQL files have been executed.")


# Verify db folder exists
db_folder = '../db'
os.makedirs(db_folder, exist_ok=True)
db_path = os.path.join(db_folder, 'example.db')

# Opens a new SQLite database
conn = sqlite3.connect(db_path)
conn.close()

# Specifies a schema directory
schemas_folder = '../schemas' 
execute_sql_files_from_folder(db_path, schemas_folder)