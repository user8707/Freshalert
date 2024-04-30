import streamlit as st
import pandas as pd
from pages import login, fresh_alert
from konstante import constants
from github_contents import GithubContents
from PIL import Image 


# Set page configuration
st.set_page_config(
    page_title="FreshAlert",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

if st.button("Home"):
    st.switch_page("Freshalert_app.py")
if st.button("Login"):
    st.switch_page("pages/login.py")
if st.button("Kühlschrank"):
    st.switch_page("pages/fresh_alert.py")


# Bildpfade
LOGO_IMAGE_PATH = "images/Logo_Freshalert-Photoroom.png"
SIDEBAR_IMAGE_PATH = "images/18-04-_2024_11-16-47-Photoroom.png"
INFO_IMAGE_PATH = "images/Foodwaste1.png"

def main():
    login.init_github()
    login.init_dataframe_login()
    login.init_dataframe_food()
    if 'user_logged_in' not in st.session_state:
        st.session_state.user_logged_in = False

    if not st.session_state.user_logged_in:
        login.show_login_page()
    else:
        fresh_alert.show_fresh_alert_page()

if __name__ == "__main__":
    main()

