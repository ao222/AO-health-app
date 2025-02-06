import streamlit as st
from FirestoreClient import FirestoreClient
import pandas as pd
from datetime import datetime
import util_time

def main():
    st.set_page_config(page_title="AO Health Tracker", page_icon="💙")
    db_client = FirestoreClient()
    st.title("Blood Pressure Data")
    
    # Date range selection
    start_date = st.date_input("Start Date", datetime.today())
    end_date = st.date_input("End Date", datetime.today())

    if st.button("Query Data"):
        # Convert dates to timestamps
        # start_timestamp = datetime.combine(start_date, datetime.min.time())
        # end_timestamp = datetime.combine(end_date, datetime.max.time())
        start_timestamp = util_time.begin_day(start_date)
        end_timestamp = util_time.end_day(end_date)
        objective_df = db_client.get_objective_snapshots(start_timestamp,end_timestamp)
        
        # Display results
        if objective_df is not None:
            st.dataframe(objective_df)
        else:
            st.write("No blood pressure data found in the selected range.")

if __name__ == "__main__":
    main()
