import streamlit as st

st.set_page_config(page_title="AO Health Tracker", page_icon="💙")

# Streamlit UI
st.title("Subjective Snapshot")

with st.form("subjective_snapshots_form"):
    date = st.date_input("Date")
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
        # insert_data(date, motivation, restfulness, irritability, social_energy, levity, productivity, appetite, psychosis, depression, mania)
        st.success("Data saved successfully!")
