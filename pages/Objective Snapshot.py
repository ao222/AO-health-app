import streamlit as st
from ..FirestoreClient import FirestoreClient

db_client = FirestoreClient()

st.title("Health Data Logger")
st.write("Enter your health metrics below:")

# Create a form
with st.form("health_form"):
    systolic = st.number_input("Systolic Blood Pressure", min_value=50, max_value=250, value=120)
    diastolic = st.number_input("Diastolic Blood Pressure", min_value=30, max_value=150, value=80)
    heart_rate = st.number_input("Heart Rate", min_value=30, max_value=200, value=72)
    glucose = st.number_input("Glucose Level", min_value=50, max_value=300, value=95)
    submit = st.form_submit_button("Submit")

if submit:
    db_client.save_objective_snapshot(systolic,diastolic,heart_rate,glucose)
    st.success("Data successfully saved!")
