import streamlit as st
import pandas as pd

# Initialize session state to store submitted data
if 'data' not in st.session_state:
    st.session_state.data = []

st.title("Streamlit Form with Table")

# Create a form with a single row for text and number input
with st.form("entry_form"):
    col1, col2 = st.columns([2, 1])  # Adjust column width ratio as needed
    with col1:
        text_input = st.text_input("Enter text:", key="text_input")
    with col2:
        number_input = st.number_input("Enter number:", step=1, key="number_input")
    submit_button = st.form_submit_button("Submit")

# Process the form submission
if submit_button:
    if text_input and number_input is not None:
        st.session_state.data.append({"Text": text_input, "Number": number_input})
        st.experimental_rerun()  # Rerun app to update the table

# Display the stored data as a table
if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)
    st.write("### Submitted Data")
    st.dataframe(df, use_container_width=True)
