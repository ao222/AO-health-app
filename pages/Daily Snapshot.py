import streamlit as st
from datetime import datetime
from FirestoreClient import FirestoreClient

# Streamlit UI
formatted_date = datetime.now().strftime("%A, %B %-d, %Y")
st.title("Daily Snapshot")
st.subheader(formatted_date)

db_client = FirestoreClient()

data = db_client.get_daily_snapshot()

with st.form("daily_snapshot"):
    date = st.date_input("Date", value=datetime.today().date())
    sleep_hours = st.number_input("Sleep (hours)", min_value=0.0, max_value=24.0, step=0.5, value=data["sleep_hours"])
    naps = st.number_input("Naps (hours)", min_value=0.0, max_value=24.0, step=0.25, value=data["naps"])
    walking_minutes = st.number_input("Walking (minutes)", min_value=0, step=5, value=data["walking_minutes"])
    lifting_minutes = st.number_input("Lifting (minutes)", min_value=0, step=5, value=data["lifting_minutes"])
    calories = st.number_input("Calories", min_value=0, step=50, value=data["calories"])
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        db_client.save_daily_snapshot(date, sleep_hours, naps, walking_minutes, lifting_minutes, calories)
        st.success("Data saved successfully!")
