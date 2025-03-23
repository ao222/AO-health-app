import streamlit as st
import pandas as pd
from FirestoreClient import FirestoreClient
import util_time

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
    db_client.save_food_snapshot(description,calories)
    
st.subheader("Today's Eats")
food_today_df = db_client.get_todays_foods()

# Display results
if food_today_df is not None:
    for index, row in food_today_df.iterrows():
        col1, col2, col3 = st.columns([3, 1, 1])  # adjust layout
        with col1:
            time = util_time.get_time(row['timestamp'])
            st.markdown(f"**{row['description']} – {row['calories']} kcal @ {time}**")
        with col2:
            if col2.button("Delete", key=f"delete_{row['timestamp']}"):
                db_client.delete_food_item(row['timestamp'])
                st.rerun()
else:
    st.write("No food snapshot data found for today.")
