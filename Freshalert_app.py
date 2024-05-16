import binascii 
import streamlit as st
import pandas as pd
import bcrypt
from github_contents import GithubContents
from PIL import Image
from datetime import datetime, timedelta
import random
import string

# Konstante für das Login
DATA_FILE = "FreshAlert-Registration.csv"
DATA_COLUMNS = ["Vorname", "Nachname", "E-Mail", "Passwort", "Passwort wiederholen", "User ID"]  

# Konstante für das Datenrepo von meinem Kühlschrank
DATA_FILE_FOOD = "Kühlschrankinhalt.csv"
DATA_COLUMNS_FOOD = ["User ID", "Lebensmittel", "Kategorie", "Lagerort", "Standort", "Ablaufdatum"] 

# Konstante für das  Datenrepo für den geteilten Kühlschrank
DATA_FILE_SHARED_FRIDGE = "geteilte_kuehlschraenke.csv"
DATA_COLUMNS_SHARED_FRIDGE = ["Kuehlschrank_ID", "User ID", "Lebensmittel", "Kategorie", "Lagerort", "Standort", "Ablaufdatum", "Tage_bis_Ablauf"]

# Load the image
image = Image.open('images/Logo_Freshalert-Photoroom.png')

# Resize the image
small_image = image.resize((90, 105))

# Set page configuration
st.set_page_config(
    page_title="FreshAlert",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

def init_dataframe_shared_fridge():
    """Initialize or load the dataframe for shared fridge contents."""
    if 'df_shared_fridge' not in st.session_state:
        if st.session_state.github.file_exists(DATA_FILE_SHARED_FRIDGE):
            st.session_state.df_shared_fridge = st.session_state.github.read_df(DATA_FILE_SHARED_FRIDGE)
        else:
            st.session_state.df_shared_fridge = pd.DataFrame(columns=DATA_COLUMNS_SHARED_FRIDGE)

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
            if row["E-Mail"] == email and bcrypt.checkpw(password.encode('utf-8'), row["Passwort"].encode('utf-8')):  # Hashed password comparison
                login_successful = True
                st.session_state.user_logged_in = True
                st.session_state.user_id = row["User ID"]  # Setze die User ID in der Session
                break
        if login_successful:
            st.success("Erfolgreich eingeloggt!")
        else:
            st.error("Ungültige E-Mail oder Passwort.")

    if not st.session_state.user_logged_in:  # Zeige den "Registrieren" Button nur wenn der Benutzer nicht eingeloggt ist
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
                # Hash the password before storing it
                hashed_password = bcrypt.hashpw(new_entry["Passwort"].encode('utf-8'), bcrypt.gensalt())
                new_entry["Passwort"] = hashed_password.decode('utf-8')
                
                # Setze die User ID als E-Mail Adresse
                new_entry["User ID"] = new_entry["E-Mail"]
                
                new_entry_df = pd.DataFrame([new_entry])
                st.session_state.df_login = pd.concat([st.session_state.df_login, new_entry_df], ignore_index=True)
                save_data_to_database_login()
                st.success("Registrierung erfolgreich!")
            else:
                st.error("Die Passwörter stimmen nicht überein.")

def show_fresh_alert_page():
    col1, col2 = st.columns([7, 1])
    col2.image(small_image, use_column_width=False, clamp=True)
    
    st.sidebar.image('images/18-04-_2024_11-16-47-Photoroom.png-Photoroom.png', use_column_width=True)

    # Create buttons for navigation
    navigation = st.sidebar.radio("Navigation", ["Startbildschirm", "Mein Kühlschrank", "Geteilter Kühlschrank", "Neues Lebensmittel hinzufügen", "Freunde einladen","Information", "Einstellungen", "Ausloggen"])

    # Check which page to display
    if navigation == "Startbildschirm":
        show_mainpage()
    elif navigation == "Mein Kühlschrank":
        show_my_fridge_page()
    elif navigation == "Geteilter Kühlschrank":
        show_shared_fridge_page()
    elif navigation == "Neues Lebensmittel hinzufügen":
        add_food_to_fridge()
    elif navigation == "Freunde einladen":
        show_my_friends()
    elif navigation == "Information":
        show_informations()
    elif navigation == "Einstellungen":
        show_settings()
    elif navigation == "Ausloggen":
        logout()
        
def generate_random_code(length=6):
    """Generate a random code of given length."""
    return ''.join(random.choices(string.digits, k=length))

def show_expired_food_on_mainpage():
    # Filtern aller Lebensmittel des aktuellen Benutzers, die bald ablaufen
    user_expired_food = st.session_state.df_food[(st.session_state.df_food['User ID'] == st.session_state.user_id) & (st.session_state.df_food['Tage_bis_Ablauf'] <= 1)]

    if not user_expired_food.empty:
        st.markdown("---")
        st.subheader("Deine Lebensmittel, welche bald ablaufen!:")
        for index, row in user_expired_food.iterrows():
            st.error(f"**{row['Lebensmittel']}** (Ablaufdatum: {row['Ablaufdatum']}, Lagerort: {row['Lagerort']})")

def show_mainpage():
    st.title("FreshAlert")
    st.subheader("Herzlich Willkommen bei FreshAlert. Deine App für deine Lebensmittel! ")            
    st.write("Füge links deine ersten Lebensmittel zu deinem Digitalen Kühlschrank hinzu. "
                 "Wir werden dich daran erinnern, es rechtzeitig zu benutzen und dir so helfen, keine Lebensmittel mehr zu verschwenden. "
                 "#StopFoodwaste ")
    # Zeigt die bald ablaufenden Lebensmittel an
    show_expired_food_on_mainpage()

def show_my_fridge_page():
    st.title("Mein Kühlschrank")

    if not st.session_state.df_food.empty:
        user_food = st.session_state.df_food[st.session_state.df_food['User ID'] == st.session_state.user_id]
        if not user_food.empty:
            st.subheader("Deine Lebensmittel im Kühlschrank:")
            st.table(user_food[['Lebensmittel', 'Kategorie', 'Lagerort', 'Standort', 'Ablaufdatum']])
        else:
            st.info("Du hast derzeit keine Lebensmittel in deinem Kühlschrank.")
    else:
        st.info("Du hast derzeit keine Lebensmittel in deinem Kühlschrank.")

def show_shared_fridge_page():
    st.title("Geteilter Kühlschrank")

    if not st.session_state.df_shared_fridge.empty:
        shared_fridge_food = st.session_state.df_shared_fridge[st.session_state.df_shared_fridge['User ID'] == st.session_state.user_id]
        if not shared_fridge_food.empty:
            st.subheader("Lebensmittel im geteilten Kühlschrank:")
            st.table(shared_fridge_food[['Kuehlschrank_ID', 'Lebensmittel', 'Kategorie', 'Lagerort', 'Standort', 'Ablaufdatum', 'Tage_bis_Ablauf']])
        else:
            st.info("Du hast derzeit keine Lebensmittel im geteilten Kühlschrank.")
    else:
        st.info("Du hast derzeit keine Lebensmittel im geteilten Kühlschrank.")

def add_food_to_fridge():
    st.title("Neues Lebensmittel hinzufügen")
    
    food_entry = {
        DATA_COLUMNS_FOOD[0]: st.session_state.user_id, # User ID
        DATA_COLUMNS_FOOD[1]: st.text_input("Lebensmittel"), 
        DATA_COLUMNS_FOOD[2]: st.text_input("Kategorie"), 
        DATA_COLUMNS_FOOD[3]: st.text_input("Lagerort"), 
        DATA_COLUMNS_FOOD[4]: st.text_input("Standort"), 
        DATA_COLUMNS_FOOD[5]: st.date_input("Ablaufdatum")
    }

    for key, value in food_entry.items():
        if value == "" and key != DATA_COLUMNS_FOOD[0]:  # Skip user ID for the empty check
            st.error(f"Bitte ergänze das Feld '{key}'")
            return
    
    if st.button("Hinzufügen"):
        food_entry["Ablaufdatum"] = food_entry["Ablaufdatum"].strftime("%Y-%m-%d")
        ablaufdatum = datetime.strptime(food_entry["Ablaufdatum"], "%Y-%m-%d")
        today = datetime.today()
        food_entry["Tage_bis_Ablauf"] = (ablaufdatum - today).days
        
        new_food_entry_df = pd.DataFrame([food_entry])
        st.session_state.df_food = pd.concat([st.session_state.df_food, new_food_entry_df], ignore_index=True)
        save_data_to_database_food()
        st.success("Lebensmittel erfolgreich hinzugefügt!")

def show_my_friends():
    st.title("Freunde einladen")
    st.write("Hier kannst du Freunde einladen und ihnen Zugriff auf deinen Kühlschrank gewähren.")

def show_informations():
    st.title("Informationen")
    st.write("Hier findest du alle wichtigen Informationen zur App.")

def show_settings():
    st.title("Einstellungen")
    if st.session_state.settings_enabled:
        st.write("Hier kannst du deine Einstellungen vornehmen.")
    else:
        st.warning("Die Einstellungen sind derzeit deaktiviert.")

def logout():
    st.session_state.user_logged_in = False
    st.session_state.user_id = None
    st.session_state.show_registration = False
    st.success("Du hast dich erfolgreich ausgeloggt.")
    show_login_page()

def save_data_to_database_login():
    """Save the login dataframe to the database."""
    st.session_state.github.write_df(st.session_state.df_login, DATA_FILE)

def save_data_to_database_food():
    """Save the food dataframe to the database."""
    st.session_state.github.write_df(st.session_state.df_food, DATA_FILE_FOOD)

def save_data_to_database_shared_fridge():
    """Save the shared fridge dataframe to the database."""
    st.session_state.github.write_df(st.session_state.df_shared_fridge, DATA_FILE_SHARED_FRIDGE)

def main():
    init_github()
    init_dataframe_login()
    init_dataframe_food()
    init_dataframe_shared_fridge()

    if 'user_logged_in' not in st.session_state:
        st.session_state.user_logged_in = False
    if st.session_state.user_logged_in:
        show_fresh_alert_page()
    else:
        show_login_page()

if __name__ == "__main__":
    main()
