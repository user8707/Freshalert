# app.py
import streamlit as st
from pages.data_management import init_dataframe_login, init_dataframe_food, save_data_to_database_login, save_data_to_database_food
from pages.github_utils import init_github
from pages.login import show_login_page, show_registration_page
from pages.fridge import show_fresh_alert_page


def main():
    st.set_page_config(page_title="FreshAlert", page_icon="🗄️", layout="wide", initial_sidebar_state="expanded")

    # Seitenleiste mit benutzerdefinierten Optionen
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Gehe zu", ["Startseite", "Kühlschrank verwalten", "Einstellungen"])

    # Funktionalitäten für die verschiedenen Seiten
    if page == "Startseite":
        show_homepage()
    elif page == "Kühlschrank verwalten":
        show_fresh_alert_page()
    elif page == "Einstellungen":
        show_settings()

def show_homepage():
    st.title("Willkommen bei FreshAlert")
    st.write("Hier ist deine Startseite. Wähle eine Option in der Seitenleiste, um fortzufahren.")

def show_fridge_management():
    st.title("Kühlschrank verwalten")
    st.write("Verwalte deinen Kühlschrankinhalt hier.")

def show_settings():
    st.title("Einstellungen")
    st.write("Passe deine Anwendungseinstellungen hier an.")

if __name__ == "__main__":
    main()
