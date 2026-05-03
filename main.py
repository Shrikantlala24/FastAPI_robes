import streamlit as st
import requests

# let's use the API in port 8009

st.title("Product Store")
if st.button('Get response'):
    res = requests.get("http://localhost:8009/about")
    res = res.json()
    st.write(f"{res['mesafe']}")

if st.button("view data"):
    res2  = requests.get("http://localhost:8009/view")
    res2 = res2.json()
    st.write(res2)


    for pid, item in res2.items():
        st.write(f"ID: {pid}")
        st.write(f"Product Name: {item['name']}")
        st.write(f"Price: {item['price']}")
        st.write("---")