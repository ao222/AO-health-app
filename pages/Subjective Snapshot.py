import streamlit as st
from FirestoreClient import FirestoreClient
import util_time

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
today_df = db_client.get_todays_subjectives()

# Display results
if today_df is not None:
    for index, row in today_df.iterrows():
        col1, col2, col3 = st.columns([3, 1, 1])  # adjust layout
        with col1:
            time = util_time.get_time(row['timestamp'])
            formatted_string = (
                f"**Motivation-{row['motivation']} | "
                f"Restfulness-{row['restfulness']} | "
                f"Irritability-{row['irritability']} | "
                f"Social Energy-{row['social_energy']} | "
                f"Levity-{row['levity']} | "
                f"Productivity-{row['productivity']} | "
                f"Appetite-{row['appetite']} | "
                f"Psychosis-{row['psychosis']} | "
                f"Depression-{row['depression']} | "
                f"Mania-{row['mania']} @ {time}**"
            )
            st.markdown(formatted_string)
        with col2:
            if col2.button("Delete", key=f"delete_{row['timestamp']}"):
                db_client.delete_subjective_snapshot(row['timestamp'])
                st.rerun()
else:
    st.write("No snapshot data found for today.")
