import streamlit as st
from FirestoreClient import FirestoreClient

# Streamlit UI
st.title("Daily Snapshot")

db_client = FirestoreClient()

with st.form("daily_snapshot"):
    date = st.date_input("Date")
    sleep_hours = st.number_input("Sleep (hours)", min_value=0.0, max_value=24.0, step=0.5)
    naps = st.number_input("Naps (hours)", min_value=0.0, max_value=24.0, step=0.25)
    walking_minutes = st.number_input("Walking (minutes)", min_value=0, step=5)
    lifting_minutes = st.number_input("Lifting (minutes)", min_value=0, step=5)
    calories = st.number_input("Calories", min_value=0, step=50)
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        db_client.save_daily_snapshot(date, sleep_hours, naps, walking_minutes, lifting_minutes, calories)
        st.success("Data saved successfully!")
