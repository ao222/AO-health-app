import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import json

# Initialize Firebase using st.secrets
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)

db = firestore.client()

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
    user_id = "user_123"  # Replace with dynamic user auth if needed
    timestamp = datetime.datetime.utcnow().isoformat()
    data = {
        "systolic": systolic,
        "diastolic": diastolic,
        "heart_rate": heart_rate,
        "glucose": glucose,
        "timestamp": timestamp
    }
    
    # Save data to Firestore
    db.collection("users").document(user_id).collection("objectives").document(timestamp).set(data)
    st.success("Data successfully saved!")
