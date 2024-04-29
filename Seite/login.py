import streamlit as st
import pandas as pd
from konstante import constants
from PIL import Image
from pages import Fresh_alert

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
    if 'df_login' not in st.session_state:
        if st.session_state.github.file_exists(DATA_FILE):
            st.session_state.df_login = st.session_state.github.read_df(DATA_FILE)
        else:
            st.session_state.df_login = pd.DataFrame(columns=DATA_COLUMNS)

def init_dataframe_food():
    """Initialize or load the dataframe for fridge contents."""
    if 'df_food' not in st.session_state:
        if st.session_state.github.file_exists(DATA_FILE_FOOD):
            st.session_state.df_food = st.session_state.github.read_df(DATA_FILE_FOOD)
        else:
            st.session_state.df_food = pd.DataFrame(columns=DATA_COLUMNS_FOOD)

def show_login_page():
    col1, col2 = st.columns([7, 1])
    col2.image(small_image, use_column_width=False, clamp=True)
    
    st.title("Welcome to FreshAlert 😀, Let's start together with saving food") 
    st.title("Login")
    email = st.text_input("E-Mail", key="login_email")
    password = st.text_input("Passwort", type="password", key="login_password")
    if st.button("Login"):
        login_successful = False
        for index, row in st.session_state.df_login.iterrows():
            if row["E-Mail"] == email and row["Passwort"] == password:
                login_successful = True
                break
        if login_successful:
            st.session_state.user_logged_in = True
            st.success("Erfolgreich eingeloggt!")
        else:
            st.error("Ungültige E-Mail oder Passwort.")
    if st.button("Registrieren", key="registration_button"):
        st.session_state.show_registration = True
    if st.session_state.get("show_registration", False):
        show_registration_page()

def show_registration_page():
    st.title("Registrieren")
           
    new_entry = {
        DATA_COLUMNS[0]: st.text_input(DATA_COLUMNS[0]), #Vorname
        DATA_COLUMNS[1]: st.text_input(DATA_COLUMNS[1]), #Nachname
        DATA_COLUMNS[2]: st.text_input(DATA_COLUMNS[2]), # E-Mail
        DATA_COLUMNS[3]: st.text_input(DATA_COLUMNS[3], type="password"), #Passwort
        DATA_COLUMNS[4]: st.text_input(DATA_COLUMNS[4], type="password"), #Passwort wiederholen
    }

    for key, value in new_entry.items():
        if value == "":
            st.error(f"Bitte ergänze das Feld '{key}'")
            return

    if st.button("Registrieren"):
        if new_entry["E-Mail"] in st.session_state.df_login["E-Mail"].values:
            st.error("Benutzer mit dieser E-Mail-Adresse ist bereits registriert.")
        else:
            if new_entry["Passwort"] == new_entry["Passwort wiederholen"]:
                new_entry_df = pd.DataFrame([new_entry])
                st.session_state.df_login = pd.concat([st.session_state.df_login, new_entry_df], ignore_index=True)
                save_data_to_database_login()
                st.success("Registrierung erfolgreich!")
                st.session_state.show_registration = False  # Reset status
            else:
                st.error("Die Passwörter stimmen nicht überein.")

def save_data_to_database_login():
    st.session_state.github.write_df(DATA_FILE, st.session_state.df_login, "Updated registration data")
