import streamlit as st
from FirestoreClient import FirestoreClient
from datetime import datetime
import util_time

db_client = FirestoreClient()
st.set_page_config(page_title="AO Health Tracker", page_icon="💙")

st.title("Objective Snapshot")

# Create a form
with st.form("health_form"):
    systolic = st.number_input("Systolic Blood Pressure", min_value=50, max_value=250, value=120)
    diastolic = st.number_input("Diastolic Blood Pressure", min_value=30, max_value=150, value=80)
    heart_rate = st.number_input("Heart Rate", min_value=30, max_value=200, value=72)
    glucose = st.number_input("Glucose Level", min_value=50, max_value=300, value=95)
    submit = st.form_submit_button("Submit")

if submit:
    db_client.save_objective_snapshot(systolic,diastolic,heart_rate,glucose)

# List todays objective snapshots for review
st.subheader("Today's Snapshots")
start_timestamp = util_time.begin_day(datetime.today())
end_timestamp = util_time.end_day(datetime.today())
today_df = db_client.get_objective_snapshots(start_timestamp,end_timestamp)

# Display results
if today_df is not None:
    st.markdown(today_df.to_markdown())
else:
    st.write("No snapshot data found for today.")

# Display results
if today_df is not None:
    for index, row in today_df.iterrows():
        col1, col2, col3 = st.columns([3, 1, 1])  # adjust layout
        with col1:
            st.markdown(f"**{row['systolic']} / {row['diastolic']} - hr: {row['heart_rate']} - glucose: {row['glucose']}**")
        with col2:
            if col2.button("Delete", key=f"delete_{row['timestamp']}"):
                # db_client.delete_food_item(row['timestamp'])
                st.rerun()
else:
    st.write("No food snapshot data found for today.")
