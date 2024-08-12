import streamlit as st
import pandas as pd

# Initialize or load the DataFrame
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['Name', 'Age'])

# Display the DataFrame
st.write("Current DataFrame:")
st.dataframe(st.session_state.df)

# Create a form
with st.form(key='my_form'):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    
    # Form submit button
    submit_button = st.form_submit_button("Submit")
    
    if submit_button:
        # Append new data to the DataFrame
        new_data = pd.DataFrame([[name, age]], columns=['Name', 'Age'])
        st.session_state.df = pd.concat([st.session_state.df, new_data], ignore_index=True)
        
        # Optionally, show a message or clear form fields
        st.success("Data added successfully!")

# Optional: Add a button to clear the DataFrame
if st.button("Clear DataFrame"):
    st.session_state.df = pd.DataFrame(columns=['Name', 'Age'])
    st.success("DataFrame cleared!")

# Refresh the displayed DataFrame
st.write("Updated DataFrame:")
st.dataframe(st.session_state.df)
