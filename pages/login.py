# login.py

import streamlit as st
import pandas as pd
from functions import init_dataframe_login, save_data_to_database_login

DATA_FILE = "FreshAlert-Registration.csv"
DATA_COLUMNS = ["Vorname", "Nachname", "E-Mail", "Passwort", "Passwort wiederholen"]

# Set constants for fridge contents
DATA_FILE_FOOD = "Kühlschrankinhalt.csv"
DATA_COLUMNS_FOOD = ["Lebensmittel", "Kategorie", "Lagerort", "Standort", "Ablaufdatum"]

image = Image.open('images/Logo_Freshalert-Photoroom.png')

# Resize the image
small_image = image.resize((90, 105))

def show_login_page(DATA_COLUMNS, small_image):
    # Initialisierung der Sitzungsvariablen, falls nicht vorhanden
    if "df_login" not in st.session_state:
        st.session_state.df_login = init_dataframe_login(DATA_FILE)
    if "user_logged_in" not in st.session_state:
        st.session_state.user_logged_in = False
    if "show_registration" not in st.session_state:
        st.session_state.show_registration = False

    col1, col2 = st.columns([7, 1])
    col2.image(small_image, use_column_width=False, clamp=True)
    
    st.title("Welcome to FreshAlert 😀, Let's start together with saving food") 
    st.title("Login")
    email = st.text_input("E-Mail", key="login_email")
    password = st.text_input("Passwort", type="password", key="login_password")
    
    # Initialisiere new_entry als leeres Dictionary
    new_entry = {}
    
    # Initialisiere login_successful
    login_successful = False
    
    if st.button("Login"):
        for index, row in st.session_state.df_login.iterrows():
            if row["E-Mail"] == email and row["Passwort"] == password:
                login_successful = True
                break  # Beende die Schleife, wenn ein erfolgreicher Login erfolgt ist
        if login_successful:
            st.session_state.user_logged_in = True
            st.success("Erfolgreich eingeloggt!")
        else:
            st.error("Ungültige E-Mail oder Passwort.")
    
    if st.button("Registrieren", key="registration_button"):
        st.session_state.show_registration = True
    
    if st.session_state.show_registration:
        show_registration_page(DATA_COLUMNS)



def show_registration_page(DATA_COLUMNS):
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
