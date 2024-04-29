import streamlit as st
import pandas as pd
import hashlib
from github_contents import GithubContents
from PIL import Image

# Set constants for user registration
DATA_FILE = "FreshAlert-Registration.csv"
DATA_COLUMNS = ["Vorname", "Nachname", "E-Mail", "Passwort", "Passwort wiederholen"]

# Set constants for fridge contents
DATA_FILE_PREFIX = "Kühlschrankinhalt_"
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

def generate_hash(data):
    # Verwende SHA-256-Hash-Funktion, um einen Hash-Code zu generieren
    hasher = hashlib.sha256()
    hasher.update(data.encode('utf-8'))
    return hasher.hexdigest()

def assign_fridge(user_email):
    # Generiere einen Hash-Code aus der Nutzer-E-Mail
    user_hash = generate_hash(user_email)
    # Verwende den Hash-Code, um den Kühlschrank des Benutzers zu identifizieren
    fridge_id = user_hash[:10]  # Verwende die ersten 10 Zeichen des Hash-Codes als Kühlschrank-ID
    return fridge_id

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
    if 'df' not in st.session_state:
        if st.session_state.github.file_exists(DATA_FILE):
            st.session_state.df_login = st.session_state.github.read_df(DATA_FILE)
        else:
            st.session_state.df_login = pd.DataFrame(columns=DATA_COLUMNS)

def init_dataframe_food(fridge_id):
    """Initialize or load the dataframe for fridge contents."""
    data_file_food = f"{DATA_FILE_PREFIX}{fridge_id}.csv"
    if 'df_food' not in st.session_state:
        if st.session_state.github.file_exists(data_file_food):
            st.session_state.df_food = st.session_state.github.read_df(data_file_food)
        else:
            st.session_state.df_food = pd.DataFrame(columns=DATA_COLUMNS_FOOD)

def show_expired_food_on_mainpage():
    # Filtern aller Lebensmittel, die rot markiert sind (Ablaufdatum erreicht oder überschritten)
    expired_food = st.session_state.df_food[st.session_state.df_food['Tage_bis_Ablauf'] <= 1]

    if not expired_food.empty:
        st.markdown("---")
        st.subheader("Deine Lebensmittel, welche bald ablaufen!:")
        for index, row in expired_food.iterrows():
            st.error(f"**{row['Lebensmittel']}** (Ablaufdatum: {row['Ablaufdatum']}, Lagerort: {row['Lagerort']})")


def show_mainpage():
    st.subheader("Herzlich Willkommen bei FreshAlert. Deine App für deine Lebensmittel! ")            
    st.write("Füge links deine ersten Lebensmittel zu deinem Digitalen Kühlschrank hinzu. "
                 "Wir werden dich daran erinnern, es rechtzeitig zu benutzen und dir so helfen, keine Lebensmittel mehr zu verschwenden. "
                 "#StopFoodwaste ")
    st.write("HALLO IHR BEIDEN 🙈")
    #Zeigt die bald ablaufenden Lebensmittel an
    show_expired_food_on_mainpage()

def colorize_expiring_food(df):
    def colorize(val):
        if val <= 1:
            return 'color: red; font-weight: bold; font-size: 14px'
        elif  val == 2 or val ==3:
            return 'color: orange; font-weight: bold; font-size: 14px'
        else:
            return 'color: green; font-weight: bold; font-size: 14px'
    
    # Berechnung der Tage bis zum Ablaufdatum
    df['Tage_bis_Ablauf'] = (pd.to_datetime(df['Ablaufdatum']) - pd.Timestamp.now()).dt.days
    df['Tage_bis_Ablauf'] = df['Tage_bis_Ablauf'].apply(lambda x: 0 if x == -1 else x)  # Setze -1 auf 0
    
    # Einfärbung der Tabellenspalten und Formatierung der Zahlen
    df_styled = df.style.applymap(colorize, subset=['Tage_bis_Ablauf']).format({'Tage_bis_Ablauf': '{:.0f}'})
    
    return df_styled

def show_my_fridge_page():
    """Display the contents of the fridge."""
    st.title("Mein Kühlschrank")
    init_dataframe_food()  # Daten laden
    
    if not st.session_state.df_food.empty:
        # Sortiere das DataFrame nach den Tagen bis zum Ablaufdatum
        st.session_state.df_food = st.session_state.df_food.sort_values(by='Tage_bis_Ablauf', ascending=True)
        
        # Colorize the expiring food entries
        df_styled = colorize_expiring_food(st.session_state.df_food)
        
        # Display the formatted DataFrame
        st.write(df_styled)
        
        # Allow the user to delete a food entry
        index_to_delete = st.number_input("Index des zu löschenden Eintrags", min_value=0, max_value=len(st.session_state.df_food)-1, step=1)
        if st.button("Eintrag löschen", key="delete_entry_button"):
            st.session_state.df_food.drop(index=index_to_delete, inplace=True)
            save_data_to_database_food()  # Save the updated dataframe
            st.success("Eintrag erfolgreich gelöscht!")
    else:
        st.write("Der Kühlschrank ist leer.")


def add_food_to_fridge():
    st.title("Neues Lebensmittel hinzufügen")
           
    new_entry = {
        DATA_COLUMNS_FOOD[0]: st.text_input(DATA_COLUMNS_FOOD[0]), #Lebensmittel
        DATA_COLUMNS_FOOD[1]: st.selectbox("Kategorie", ["Bitte wählen","Gemüse", "Obst", "Milchprodukte", "Fleisch", "Fisch", "Eier", "Getränke", "Saucen", "Getreideprodukte", "Tiefkühlprodukte"]), #Kategorie
        DATA_COLUMNS_FOOD[2]: st.selectbox("Lagerort", ["Bitte wählen", "Schrank", "Kühlschrank", "Tiefkühler", "offen"]), # Location
        DATA_COLUMNS_FOOD[3]: st.selectbox("Standort", ["Bitte wählen", "Mein Kühlschrank", "geteilter Kühlschrank"]), #area
        DATA_COLUMNS_FOOD[4]: st.date_input("Ablaufdatum"), #Ablaufdatum
    }

    for key, value in new_entry.items():
        if value == "":
            st.error(f"Bitte ergänze das Feld '{key}'")
            return

    if st.button("Hinzufügen"):
        new_entry_df = pd.DataFrame([new_entry])
        st.session_state.df_food = pd.concat([st.session_state.df_food, new_entry_df], ignore_index=True)
        save_data_to_database_food()
        st.success("Lebensmittel erfolgreich hinzugefügt!")


def save_data_to_database_food():
    if 'github' in st.session_state:
        fridge_id = st.session_state.fridge_id
        data_file_food = f"{DATA_FILE_PREFIX}{fridge_id}.csv"
        st.session_state.github.write_df(data_file_food, st.session_state.df_food, "Updated food data")


def show_settings():
    st.title("Einstellungen")

def show_my_friends():
    st.title("Lade meine Freunde ein")

def show_informations():
    st.title("Was ist Foodwaste?")
    st.image ("Foodwaste1.png")
    

def save_data_to_database_login():
    st.session_state.github.write_df(DATA_FILE, st.session_state.df_login, "Updated registration data")

def logout():
    """Logout function to reset user session and redirect to login page."""
    st.session_state.user_logged_in = False
    st.success("Erfolgreich ausgeloggt!")
    st.experimental_rerun()  # Rerun the app to go back to the login page

def main():
    init_github()
    init_dataframe_login()
    if 'user_logged_in' not in st.session_state:
        st.session_state.user_logged_in = False

    if not st.session_state.user_logged_in:
        show_login_page()
    else:
        show_fresh_alert_page()

if __name__ == "__main__":
    main() 


