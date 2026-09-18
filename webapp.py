import streamlit as st
import plotly.express as px
import sqlite3
import threading

conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("SELECT date FROM global_temps")
dates = cursor.fetchall()
dates = [item[0] for item in dates]
print(dates)

cursor.execute("SELECT temperature FROM global_temps")
temperatures = cursor.fetchall()
temperatures = [item[0] for item in temperatures]
print(temperatures)

figure1 = px.line(x=dates, y=temperatures,
                  labels={"x": "Date", "y": "Temperature (C)"})
st.plotly_chart(figure1)