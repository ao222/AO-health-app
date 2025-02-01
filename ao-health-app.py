import streamlit as st
import sqlite3
from datetime import datetime

# Using @st.cache_resource ensures that the DB connection
# is only created once per session on Streamlit Community Cloud.
@st.cache_resource
def init_connection():
    conn = sqlite3.connect('health_data.db')
    return conn

conn = init_connection()
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS health_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        mood INTEGER,
        symptoms TEXT,
        productivity INTEGER
    )
''')
conn.commit()

st.title("Health Tracking App")

# --- Form to submit data ---
with st.form("health_form"):
    st.write("Enter your health info for today:")

    # Mood (1-10)
    mood = st.slider("Mood (1-10)", 1, 10, 5)
    # Symptoms
    symptoms = st.text_input("Symptoms")
    # Productivity (1-10)
    productivity = st.slider("Productivity (1-10)", 1, 10, 5)

    # Submit button
    submitted = st.form_submit_button("Save Entry")
    if submitted:
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("""
            INSERT INTO health_data (date, mood, symptoms, productivity)
            VALUES (?, ?, ?, ?)
        """, (date_str, mood, symptoms, productivity))
        conn.commit()
        st.success("Entry saved!")

st.write("---")

# --- Display saved data ---
st.subheader("Previous Entries")
c.execute("SELECT date, mood, symptoms, productivity FROM health_data ORDER BY id DESC")
rows = c.fetchall()

if not rows:
    st.write("No entries yet. Add an entry above.")
else:
    st.table(rows)
