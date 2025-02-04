import streamlit as st

st.title("Editable Table")

    # Initialize session state
    if "table_data" not in st.session_state:
        st.session_state.table_data = pd.DataFrame({"Label": [""], "Value": [0]})

    # Editable table
    edited_df = st.data_editor(st.session_state.table_data, num_rows="dynamic", key="table_editor")

    # Update session state with edited data
    st.session_state.table_data = edited_df

    # Submit button
    if st.button("Submit"):
        st.write("Submitted Data:", st.session_state.table_data)
