import streamlit as st
import pandas as pd
from github_contents import GithubContents

st.set_page_config(page_title="FreshAlert", page_icon="🗄️", layout="wide")

def main():
    if not is_user_logged_in():
        show_login_page()
    else:
        show_fresh_alert_page()
def is_user_logged_in():
    return True  # Für dieses Beispiel gehe ich davon aus, dass der Benutzer nicht eingeloggt ist
   

def show_login_page():
    st.title("Login")
    email = st.text_input("E-Mail", key="login_email")
    password = st.text_input("Passwort", type="password", key="login_password")
    if st.button("Login"):
        if email == "example@example.com" and password == "password":
            st.success("Erfolgreich eingeloggt!")
            show_fresh_alert_page()
        else:
            st.error("Ungültige E-Mail oder Passwort.")
    if st.button("Registrieren", key="registration_button"):
        st.session_state.show_registration = True
    if st.session_state.get("show_registration", False):
        with st.sidebar:
            show_registration_page()
def show_fresh_alert_page():
    st.title("FreshAlert")
    st.sidebar.title("")
    if st.sidebar.button("Mein Kühlschrank"):
        show_my_fridge()
    if st.sidebar.button("Neues Lebensmittel hinzufügen"):
        add_new_food()
    st.sidebar.markdown("---")  # Trennlinie
    if st.sidebar.button("Freunde einladen"):
        show_my_friends()
    if st.sidebar.button("Einstellungen"):
        show_settings()
def show_my_fridge():
    st.title("Mein Kühlschrank")
    if "my_fridge" not in st.session_state:
        st.session_state.my_fridge = pd.DataFrame(columns=["Lebensmittel", "Kategorie", "Lagerort", "Ablaufdatum"])
    st.write(st.session_state.my_fridge)
def add_new_food():
    st.title("Neues Lebensmittel hinzufügen")
    with st.form("new_food_form"):
        st.write("Füllen Sie die folgenden Felder aus:")
        food_name = st.text_input("Lebensmittel", key="food_name")
        category = st.selectbox("Kategorie", ["Gemüse", "Obst", "Milchprodukte", "Fleisch", "Fisch", "Eier", "Getränke", "Saucen", "Getreideprodukte", "Tiefkühlprodukte"], key="food_category")
        location = st.selectbox("Lagerort", ["Schrank", "Kühlschrank", "Tiefkühler", "offen"], key="food_location")
        expiry_date = st.date_input("Ablaufdatum", key="food_expiry_date")
        submitted = st.form_submit_button("Hinzufügen")
        if submitted:
            if "my_fridge" not in st.session_state:
                st.session_state.my_fridge = []
            st.session_state.my_fridge.append(
                (food_name, category, location, expiry_date)
            )
            st.session_state.my_fridge = pd.DataFrame(
                st.session_state.my_fridge,
                columns=["Lebensmittel", "Kategorie", "Lagerort", "Ablaufdatum"],
            )
            # Zeige die Tabelle mit den Lebensmitteln an
            st.write(st.session_state.my_fridge)
def show_my_friends():
    st.write("Meine Freunde")
def show_settings():
    st.write("Einstellungen")
def show_registration_page():
    st.title("Registrieren")
    first_name = st.text_input("Vorname", key="register_first_name")
    last_name = st.text_input("Nachname", key="register_last_name")
    email = st.text_input("E-Mail", key="register_email")
    password = st.text_input("Passwort", type="password", key="register_password")
    confirm_password = st.text_input("Passwort wiederholen", type="password", key="confirm_register_password")
   # Registrierungs-Button
    if st.button("Registrieren"):
        if password == confirm_password:
            st.success("Registrierung erfolgreich!")
            st.session_state.show_registration = False  # Setze den Status zurück
        else:
            st.error("Die Passwörter stimmen nicht überein.")

if __name__ == "__main__":

    main()
    
st.text('Herzlich Willkommen bei FreshAlert. Deine App für deine Lebensmittel!')
st.text('Füge links deine ersten Lebensmittel zu deinem Digitalen Kühlschrank hinzu.')
st.text('Wir werden dich daran erinnen, es rechtzeitig zu benutzen 
und dir so helfen keine Lebensmittel mehr zu verschwenden.')
st.text('#StopFoodwaste')
