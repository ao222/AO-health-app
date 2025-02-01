import streamlit as st
import sqlite3
from datetime import datetime
from google.oauth2 import id_token
from google.auth.transport import requests
import os

# --- CONFIGURATION ---
GOOGLE_CLIENT_ID = st.secrets["google_api_key"]
ALLOWED_EMAIL = st.secrets["my_email"]
DB_PATH = st.secrets["db_path"]

# --- AUTHENTICATION FUNCTION ---
def verify_google_oauth(token):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        if idinfo['email'] == ALLOWED_EMAIL:
            return True
    except Exception as e:
        return False
    return False

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS health_data (
                        date TEXT PRIMARY KEY, 
                        weight REAL, 
                        sleep_hours REAL, 
                        water_intake REAL)''')
    conn.commit()
    conn.close()

# --- SAVE DATA FUNCTION ---
def save_data(date, weight, sleep_hours, water_intake):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''INSERT OR REPLACE INTO health_data (date, weight, sleep_hours, water_intake) 
                      VALUES (?, ?, ?, ?)''', (date, weight, sleep_hours, water_intake))
    conn.commit()
    conn.close()

# --- LOAD DATA FUNCTION ---
def load_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM health_data ORDER BY date DESC")
    data = cursor.fetchall()
    conn.close()
    return data

# --- STREAMLIT UI ---
st.title("📊 Personal Health Tracker")

# Google OAuth Token Input
token = st.text_input("Paste your Google OAuth Token here:", type="password")
if token and verify_google_oauth(token):
    st.success("Authentication Successful!")
    init_db()

    # --- Input Form ---
    st.subheader("Log Your Health Data")
    date = st.date_input("Date", datetime.today()).strftime('%Y-%m-%d')
    weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
    sleep_hours = st.number_input("Sleep Hours", min_value=0.0, step=0.1)
    water_intake = st.number_input("Water Intake (L)", min_value=0.0, step=0.1)

    if st.button("Save Data"):
        save_data(date, weight, sleep_hours, water_intake)
        st.success("Data Saved!")

    # --- Display Data ---
    st.subheader("Your Health Data")
    data = load_data()
    if data:
        st.write("### Data Table")
        st.dataframe(data, columns=["Date", "Weight (kg)", "Sleep Hours", "Water Intake (L)"])
    else:
        st.write("No data available yet.")
else:
    st.warning("Please authenticate using Google OAuth token.")
