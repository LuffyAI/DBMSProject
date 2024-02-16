## Author: Larnell Moore
## Creation Date: Feb 14 2024
## Purpose: Launches the Flask web app.

from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world!"

if __name__ == "__main__":  
    app.run()
