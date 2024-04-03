import sqlite3
import os

db_path = 'flask-backend/RecallDb.db'

def execute_sql_file(cursor, filepath):
    with open(filepath, 'r') as file:
        sql_script = file.read()
    cursor.executescript(sql_script)

# Check if the database already exists and remove it
if os.path.exists(db_path):
    os.remove(db_path)

# Connect to SQLite (this will create a new database)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Enable foreign key constraint enforcement
cursor.execute("PRAGMA foreign_keys = ON;")

# Execute SQL files in the required order
files_to_execute = ['sql/tables.sql', 'sql/triggers.sql', 'sql/insertions.sql']
for file in files_to_execute:
    execute_sql_file(cursor, file)

conn.commit()
conn.close()
