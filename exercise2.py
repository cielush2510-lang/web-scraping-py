import sqlite3

conn = sqlite3.connect('data.db', check_same_thread=False)
cursor = conn.cursor()

# Query ALL columns for filter
cursor.execute("SELECT * FROM events WHERE band='A7X'")
rows = cursor.fetchall()
print(rows)

# Query specific columns for filter
cursor.execute("SELECT band, date FROM events WHERE band='A7X'")
rows = cursor.fetchall()
print(rows)

# insert new rows
new_rows = [("Beatles", "London", "2088.10.15"),
            ("Coldplay", "Munich", "2088.10.17")]

cursor.executemany("INSERT INTO events (band, city, date) VALUES (?,?,?)", new_rows)
conn.commit()

# Query last two rows and reverse the order so it shows the last two rows from newest > oldest
cursor.execute("SELECT * FROM (SELECT * FROM events ORDER BY event_id DESC LIMIT 2) AS last_events ORDER BY event_id ASC")
rows = cursor.fetchall()
print(rows)

# Query all data
cursor.execute("SELECT * FROM events")
rows = cursor.fetchall()
print(rows)