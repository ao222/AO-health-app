import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from datetime import datetime

def main():
    st.title("Blood Pressure Data")
    
    # Date range selection
    start_date = st.date_input("Start Date", datetime.today())
    end_date = st.date_input("End Date", datetime.today())

    if st.button("Query Data"):
        # Convert dates to timestamps
        start_timestamp = datetime.combine(start_date, datetime.min.time())
        end_timestamp = datetime.combine(end_date, datetime.max.time())
    
        db_client = init_firestore_client()
        data = query_db(db_client,start_timestamp,end_timestamp)
        
        # Display results
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.write("No blood pressure data found in the selected range.")


def init_firestore_client():
    # Initialize Firebase
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
        firebase_admin.initialize_app(cred)

    # Firestore client
    db = firestore.client(database_id="ao-health-data")
    return db

def query_db(db,start_date_stamp,end_date_stamp):
    # Query Firestore
    objective_snapshot_ref = db.collection("users").document("user_123").collection("objectives")
    # query = objective_snapshot_ref.where("timestamp", ">=", start_date_stamp).where("timestamp", "<=", end_date_stamp)
    query = objective_snapshot_ref.get()
    # docs = query.stream()

    # Process results
    data = []
    for doc in query:
        doc_data = doc.to_dict()
        data.append({
            "Systolic": doc_data.get("systolic"),
            "Diastolic": doc_data.get("diastolic"),
            "HeartRate": doc_data.get("heart_rate"),
            "Glucose": doc_data.get("glucose"),
            "Timestamp": doc_data.get("timestamp")
        })
    return data

if __name__ == "__main__":
    main()
