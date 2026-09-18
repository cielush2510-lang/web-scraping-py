import threading

import requests, ssl, smtplib
import sqlite3
import selectorlib
import os
import time

URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

_SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    band TEXT NOT NULL,
    city TEXT NOT NULL,
    date TEXT NOT NULL
);
"""

class Event:
    def scrape(self, url):
        """Scrape the page source from the URL"""
        source = requests.get(url, headers=HEADERS).text
        return source


    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value


class Email:
    def send(self, message):
        print("Sending email...")
        host = "smtp.gmail.com"
        port = 465

        username = "cielush2510@gmail.com"
        password = "ygxbauweewzdiutm"

        receiver = "cielush2510@gmail.com"
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, receiver, message)

        print("Email sent!")

class Database:

    def __init__(self, database_path):
        self.conn = sqlite3.connect(database_path, check_same_thread=False)
        self.lock = threading.Lock()
        with self.lock:
            self.conn.execute(_SCHEMA)
            self.conn.commit()

    def store(self, extracted):
        row = extracted.split(",")
        row = [item.strip() for item in row]
        cursor = self.conn.cursor()
        with self.lock:
            cursor.execute("INSERT INTO events (band, city, date) VALUES (?,?,?)", row)
            self.conn.commit()



    def read(self, extracted):
         row = extracted.split(",")
         row = [item.strip() for item in row]
         band, city, date = row
         cursor = self.conn.cursor()
         with self.lock:
             cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
             rows = cursor.fetchall()
         print(rows)
         return rows


if __name__ == "__main__":
    while True:
        event = Event()
        scraped = event.scrape(URL)
        extracted = event.extract(scraped)
        print(extracted)

        if extracted != "No upcoming tours":
            database = Database(database_path="data.db")
            row = database.read(extracted)
            if not row:
                database.store(extracted)
                email = Email()
                email.send(message="Hey, new event was found!")
        time.sleep(2)