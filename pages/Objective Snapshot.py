# streamlit_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read()

# Print results.
# col names: Stamp	Systolic	Diastolic	Heart Rate	Glucose
for row in df.itertuples():
    st.write(f"{row.Stamp} glucose :{row.Glucose}:")
