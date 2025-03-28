import streamlit as st
from FirestoreClient import FirestoreClient
import util_time

# Streamlit UI
st.set_page_config(page_title="AO Health Tracker", page_icon="💙")
formatted_date = util_time.get_today_formatted()
st.title("Daily Snapshot")
st.subheader(formatted_date)

db_client = FirestoreClient()

data = db_client.get_daily_snapshot()

if data is None:
    data = {
            "sleep_hours": 0.0,
            "naps": 0.0,
            "walking_minutes": 0,
            "lifting_minutes": 0,
            "calories": 0,
            "caffeine": 0
    }
with st.form("daily_snapshot"):
    sleep_hours = st.number_input("Sleep (hours)", min_value=0.0, max_value=24.0, step=0.5, value=data["sleep_hours"])
    naps = st.number_input("Naps (hours)", min_value=0.0, max_value=24.0, step=0.25, value=data["naps"])
    walking_minutes = st.number_input("Walking (minutes)", min_value=0, step=5, value=data["walking_minutes"])
    lifting_minutes = st.number_input("Lifting (minutes)", min_value=0, step=5, value=data["lifting_minutes"])
    calories = st.number_input("Calories", min_value=0, step=50, value=data["calories"])
    caffeine = st.number_input("Caffeine", min_value=0, step=5, value=data["caffeine"])
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        db_client.save_daily_snapshot(sleep_hours, naps, walking_minutes, lifting_minutes, calories, caffeine)
        st.success("Data saved successfully!")
