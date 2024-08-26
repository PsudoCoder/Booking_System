import streamlit as st
import requests

API_URL = "https://qcdue3ihel.execute-api.eu-north-1.amazonaws.com/prod/auth"

def authenticate_user(username: str, password: str) -> bool:
    response = requests.post(API_URL, json={'username': username, 'password': password})
    return response.status_code == 200

@st.dialog("Admin Login")
def show_login():
    st.title("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state.logged_in = True
            st.session_state.page = "Admin Dashboard"
            st.rerun()
        else:
            st.error("Invalid username or password")
