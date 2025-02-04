import streamlit as st
import pandas as pd

st.title("Food Snapshot")

with st.form("input_form"):
    col1, col2 = st.columns([3, 1])  # Adjust ratio to control space allocation
    
    with col1:
        text_input = st.text_input("Food description")
    with col2:
        numeric_input = st.number_input("Num calories", min_value=0, step=1)
    
    submit_button = st.form_submit_button("Submit")

if submit_button:
    st.write(f"Text: {text_input}")
    st.write(f"Number: {numeric_input}")
