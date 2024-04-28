# app.py
import streamlit as st
from pages.data_management import init_dataframe_login, init_dataframe_food, save_data_to_database_login, save_data_to_database_food
from pages.github_utils import init_github
from pages.login import show_login_page, show_registration_page
from pages.fridge import show_fresh_alert_page, show_mainpage, show_my_fridge_page, add_food_to_fridge, show_my_friends, show_settings


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
