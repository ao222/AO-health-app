import streamlit as st

st.title("Dynamic Form")

if "fields" not in st.session_state:
    st.session_state.fields = [("", 0)]

def add_field():
    st.session_state.fields.append(("", 0))

def remove_field(index):
    if len(st.session_state.fields) > 1:
        del st.session_state.fields[index]

with st.form("dynamic_form"):
    new_fields = []
    for i, (text, number) in enumerate(st.session_state.fields):
        col1, col2, col3 = st.columns([3, 1, 0.5])  # Adjust column ratios
        text_value = col1.text_input(f"Label {i+1}", value=text, key=f"text_{i}")
        number_value = col2.number_input(f"Value {i+1}", value=number, key=f"num_{i}")
        if col3.button("❌", key=f"remove_{i}"):
            remove_field(i)
        new_fields.append((text_value, number_value))
    
    st.session_state.fields = new_fields
    
    st.form_submit_button("Submit")
    
if st.button("+ Add Another Field"):
    add_field()
