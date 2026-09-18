import threading
from datetime import datetime
import requests, ssl, smtplib
import sqlite3
import selectorlib
import os
import time

_SCHEMA = """
CREATE TABLE IF NOT EXISTS global_temps (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    temperature FLOAT NOT NULL
);
"""

URL = "https://programmer100.pythonanywhere.com"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

conn = sqlite3.connect('data.db', check_same_thread=False)
lock = threading.Lock()
with lock:
    conn.execute(_SCHEMA)
    conn.commit()

def scrape(url):
    source = requests.get(URL, headers=HEADERS).text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("exercise.yaml")
    value = extractor.extract(source)["temps"]
    return value



def store(extracted):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor = conn.cursor()
    with lock:
        cursor.execute("INSERT INTO global_temps (date, temperature) VALUES (?,?)", (now, extracted))
        conn.commit()



def read(extracted):
    with open("ep_data.txt", "r") as file:
        return file.read()


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        store(extracted)

        time.sleep(5)