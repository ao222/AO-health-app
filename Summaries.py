import streamlit as st
from FirestoreClient import FirestoreClient
import pandas as pd
from datetime import datetime

def main():
    db_client = FirestoreClient()
    st.title("Blood Pressure Data")
    
    # Date range selection
    start_date = st.date_input("Start Date", datetime.today())
    end_date = st.date_input("End Date", datetime.today())

    if st.button("Query Data"):
        # Convert dates to timestamps
        start_timestamp = datetime.combine(start_date, datetime.min.time())
        end_timestamp = datetime.combine(end_date, datetime.max.time())
        objective_df = db_client.get_all_objective_snapshots()
        
        # Display results
        if data:
            st.dataframe(objective_df)
        else:
            st.write("No blood pressure data found in the selected range.")

if __name__ == "__main__":
    main()
