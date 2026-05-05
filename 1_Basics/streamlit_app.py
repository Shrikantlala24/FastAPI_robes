import streamlit as st
import requests

st.title("API testing and overview")

name = st.text_input('Enter your name')
if st.button('Check response'):
    response = requests.get('http://localhost:8000/')
    data = response.json()
    st.write(f"{data}")

if st.button('check trial get'):
    response2 = requests.get("http://localhost:8000/hutt")
    data2 = response2.json()
    st.write(f'{data2}')