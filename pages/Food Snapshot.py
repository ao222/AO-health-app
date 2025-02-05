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
    db_client.save_food_snapshot(description,calories)
    
st.subheader("Today's Eats")
food_today_df = db_client.get_today_food_snapshots()

# Display results
if food_today_df is not None:
    st.markdown(food_today_df.to_markdown())
else:
    st.write("No food snapshot data found for today.")

# Create a form for deleting a line item of food
with st.form(key='my_form'):
    line_number = st.number_input('Food Item', min_value=0, step=1)
    clear_button = st.form_submit_button(label='Clear')

# Handle form submission
if clear_button:
    st.write(f'Line number submitted: {line_number}')
    # Add your clearing logic here, if needed
