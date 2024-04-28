# app.py
import streamlit as st
from data_management import * 
from github_utils import *
from pages import *

def main():
    st.set_page_config(
        page_title="FreshAlert",
        page_icon="🗄️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    init_github()
    init_dataframe_login()
    init_dataframe_food()
    
    if 'user_logged_in' not in st.session_state:
        st.session_state.user_logged_in = False

    if not st.session_state.user_logged_in:
        show_login_page()
    else:
        show_fresh_alert_page()

if __name__ == "__main__":
    main()
