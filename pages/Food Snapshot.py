import streamlit as st
import pandas as pd
from FirestoreClient import FirestoreClient

db_client = FirestoreClient()
st.set_page_config(page_title="AO Health Tracker", page_icon="💙")

st.title("Food Snapshot")

with st.form("input_form"):
    col1, col2 = st.columns([3, 1])  # Adjust ratio to control space allocation
    
    with col1:
        description = st.text_input("Food description")
    with col2:
        calories = st.number_input("Num calories", min_value=0, step=1)
    
    submit_button = st.form_submit_button("Submit")

if submit_button:
    db_client.save_foods_snapshot(description,calories)
    
