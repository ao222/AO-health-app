import streamlit as st
from FirestoreClient import FirestoreClient
import pandas as pd
from datetime import datetime
import util_time

def main():
    st.set_page_config(page_title="AO Health Tracker", page_icon="💙")
    db_client = FirestoreClient()
    st.title("Data Summaries")
    
    st.markdown("Summaries to go here. . .")

if __name__ == "__main__":
    main()
