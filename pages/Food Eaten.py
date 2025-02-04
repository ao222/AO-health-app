import streamlit as st
import pandas as pd

with tab_df:
    st.write('# Solution using a dataframe')

    # Create an empty dataframe on first page load, will skip on page reloads
    if 'data' not in st.session_state:
        data = pd.DataFrame({'col1':[],'col2':[],'col3':[],'col4':[]})
        st.session_state.data = data

    # Show current data
    st.dataframe(st.session_state.data)

    st.write('#### Using form submission')

    # Function to append inputs from form into dataframe
    def add_dfForm():
        row = pd.DataFrame({'col1':[st.session_state.input_df_form_col1],
                'col2':[st.session_state.input_df_form_col2],
                'col3':[st.session_state.input_df_form_col3],
                'col4':[st.session_state.input_df_form_col2-st.session_state.input_df_form_col3]})
        st.session_state.data = pd.concat([st.session_state.data, row])

    # Inputs listed within a form
    dfForm = st.form(key='dfForm', clear_on_submit=True)
    with dfForm:
        dfFormColumns = st.columns(4)
        with dfFormColumns[0]:
            st.text_input('col1', key='input_df_form_col1')
        with dfFormColumns[1]:
            st.number_input('col2', step=1, key='input_df_form_col2')
        with dfFormColumns[2]:
            st.number_input('col3', step=1, key='input_df_form_col3')
        with dfFormColumns[3]:
            pass
        st.form_submit_button(on_click=add_dfForm)

    st.write('#### Not using form submission')

    # Function to append non-form inputs into dataframe
    def add_df():
        row = pd.DataFrame({'col1':[st.session_state.input_df_col1],
                'col2':[st.session_state.input_df_col2],
                'col3':[st.session_state.input_df_col3],
                'col4':[st.session_state.input_df_col2-st.session_state.input_df_col3]})
        st.session_state.data = pd.concat([st.session_state.data, row])

    # Inputs created outside of a form (allows computing col4 for preview)
    dfColumns = st.columns(4)
    with dfColumns[0]:
        st.text_input('col1', key='input_df_col1')
    with dfColumns[1]:
        st.number_input('col2', step=1, key='input_df_col2')
    with dfColumns[2]:
        st.number_input('col3', step=1, key='input_df_col3')
    with dfColumns[3]:
        st.number_input('col4', step=1, key='input_df_col4', 
                        value = st.session_state.input_df_col2-st.session_state.input_df_col3, 
                        disabled=True)
    st.button('Submit', on_click=add_df)
