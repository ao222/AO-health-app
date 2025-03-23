import streamlit as st
from FirestoreClient import FirestoreClient
import util_time
from datetime import datetime

db_client = FirestoreClient()
st.set_page_config(page_title="AO Health Tracker", page_icon="💙")

# Streamlit UI
st.title("Subjective Snapshot")

with st.form("subjective_snapshots_form"):
    motivation = st.slider("Motivation", 0, 10, 5)
    restfulness = st.slider("Restfulness", 0, 10, 5)
    irritability = st.slider("Irritability", 0, 10, 5)
    social_energy = st.slider("Social Energy", 0, 10, 5)
    levity = st.slider("Levity", 0, 10, 5)
    productivity = st.slider("Productivity", 0, 10, 5)
    appetite = st.slider("Appetite", 0, 10, 5)
    psychosis = st.slider("Psychosis", 0, 10, 0)
    depression = st.slider("Depression", 0, 10, 0)
    mania = st.slider("Mania", 0, 10, 0)
    
    submitted = st.form_submit_button("Submit")
    
if submitted:
    db_client.save_subjective_snapshot(motivation, restfulness, irritability, social_energy, levity, productivity, appetite, psychosis, depression, mania)

# List todays objective snapshots for review
st.subheader("Today's Snapshots")
start_timestamp = util_time.begin_day(datetime.today())
end_timestamp = util_time.end_day(datetime.today())
today_df = db_client.get_subjective_snapshots(start_timestamp,end_timestamp)

# Display results
if today_df is not None:
    for index, row in today_df.iterrows():
        col1, col2, col3 = st.columns([3, 1, 1])  # adjust layout
        with col1:
            time = util_time.get_time(row['timestamp'])
            # st.markdown(f"**{row['systolic']} / {row['diastolic']} - hr: {row['heart_rate']} - glucose: {row['glucose']} @ {time}**")
            st.markdown(f"** @ {time}**")
        with col2:
            if col2.button("Delete", key=f"delete_{row['timestamp']}"):
                db_client.delete_subjective_snapshot(row['timestamp'])
                st.rerun()
else:
    st.write("No snapshot data found for today.")
