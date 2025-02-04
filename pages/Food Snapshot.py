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
st.dataframe(food_today_df)
"""
import streamlit as st

if "rows" not in st.session_state:
    st.session_state.rows = [{"text": "Row 1", "number": 10}]

def delete_row(index):
    st.session_state.rows.pop(index)
    st.experimental_rerun()

st.write("### Editable Table")

for i, row in enumerate(st.session_state.rows):
    cols = st.columns([2, 1, 0.5])  # Text, Number, Delete
    row["text"] = cols[0].text_input(f"Text {i}", value=row["text"], key=f"text_{i}")
    row["number"] = cols[1].number_input(f"Number {i}", value=row["number"], key=f"num_{i}")
    if cols[2].button("❌", key=f"del_{i}"):
        delete_row(i)

if st.button("Add Row"):
    st.session_state.rows.append({"text": "", "number": 0})
    st.experimental_rerun()
"""
