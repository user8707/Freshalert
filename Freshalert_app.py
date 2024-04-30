import streamlit as st
import pandas as pd
from pages.github_contents import GithubContents
from PIL import Image
from pages import login, fresh_alert

# Set constants for user registration
DATA_FILE = "FreshAlert-Registration.csv"
DATA_COLUMNS = ["Vorname", "Nachname", "E-Mail", "Passwort", "Passwort wiederholen"]

# Set constants for fridge contents
DATA_FILE_FOOD = "Kühlschrankinhalt.csv"
DATA_COLUMNS_FOOD = ["Lebensmittel", "Kategorie", "Lagerort", "Standort", "Ablaufdatum"]

# Load the image
image = Image.open('Logo_Freshalert-Photoroom.png')

# Resize the image
small_image = image.resize((90, 105))

# Set page configuration
st.set_page_config(
    page_title="FreshAlert",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Initialize GithubContents object and other session state variables
    init_github()

    # Initialize or load the dataframe for user registration
    init_dataframe_login()

    # Initialize or load the dataframe for fridge contents
    init_dataframe_food()

    if 'user_logged_in' not in st.session_state:
        st.session_state.user_logged_in = False

    if not st.session_state.user_logged_in:
        # Show login page if user is not logged in
        login.show_login_page()
    else:
        # Show fresh alert page if user is logged in
        fresh_alert.show_fresh_alert_page()

def init_github():
    """Initialize the GithubContents object and other session state variables."""
    if 'github' not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"]
        )

    # Initialize settings_enabled attribute
    if 'settings_enabled' not in st.session_state:
        st.session_state.settings_enabled = True

def init_dataframe_login():
    """Initialize or load the dataframe for user registration."""
    login.init_dataframe_login()

def init_dataframe_food():
    """Initialize or load the dataframe for fridge contents."""
    fresh_alert.init_dataframe_food()

if __name__ == "__main__":
    main()
