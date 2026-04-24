import streamlit as st
import requests

st.title("API testing and overview")

name = st.text_input('Enter your name')
if st.button('Check response'):
    response = requests.get('http://localhost:8000/')
    data = response.json()
    st.write(f"{data}")