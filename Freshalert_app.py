import streamlit as st
import pandas as pd
from github_contents import GithubContents

# Set constants for user registration
DATA_FILE = "FreshAlert-Registration.csv"
DATA_COLUMNS = ["Vorname", "Nachname", "E-Mail", "Passwort", "Passwort wiederholen"]

# Set constants for fridge contents
DATA_FILE_FOOD = "FridgeContents.csv"
DATA_COLUMNS_FOOD = ["Lebensmittel", "Kategorie", "Lagerort", "Ablaufdatum", "Standort"]

# Set page configuration
st.set_page_config(
    page_title="FreshAlert",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def init_github():
    """Initialize the GithubContents object."""
    if 'github' not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"]
        )

def init_dataframe_login():
    """Initialize or load the dataframe for user registration."""
    if 'df' not in st.session_state:
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
        if new_entry["Passwort"] == new_entry["Passwort wiederholen"]:
            new_entry_df = pd.DataFrame([new_entry])
            st.session_state.df_login = pd.concat([st.session_state.df_login, new_entry_df], ignore_index=True)
            save_data_to_database_login()
            st.success("Registrierung erfolgreich!")
            st.session_state.show_registration = False  # Reset status
        else:
            st.error("Die Passwörter stimmen nicht überein.")

def show_my_fridge():
    st.title("Lebensmittel hinzufügen")
           
    new_entry = {
        DATA_COLUMNS_FOOD[0]: st.text_input(DATA_COLUMNS_FOOD[0]), #Lebensmittel
        DATA_COLUMNS_FOOD[1]: st.text_input(DATA_COLUMNS_FOOD[1]), #Kategorie
        DATA_COLUMNS_FOOD[2]: st.text_input(DATA_COLUMNS_FOOD[2]), # Lagerort
        DATA_COLUMNS_FOOD[3]: st.text_input(DATA_COLUMNS_FOOD[3], type="date"), #Ablaufdatum
        DATA_COLUMNS_FOOD[4]: st.text_input(DATA_COLUMNS_FOOD[4],), #Standort
    }

    for key, value in new_entry.items():
        if value == "":
            st.error(f"Bitte ergänze das Feld '{key}'")
            return

    if st.button("hinzufügen"):
        if new_entry["Passwort"] == new_entry["Passwort wiederholen"]:
            new_entry_df = pd.DataFrame([new_entry])
            st.session_state.df_login = pd.concat([st.session_state.df_login, new_entry_df], ignore_index=True)
            save_data_to_database_login()
            st.success("Registrierung erfolgreich!")
            st.session_state.show_registration = False  # Reset status
        else:
            st.error("Die Passwörter stimmen nicht überein.")


def show_fresh_alert_page():
    st.title("FreshAlert")
    st.subheader("Herzlich Willkommen bei FreshAlert. Deine App für deine Lebensmittel! "            
"Füge links deine ersten Lebensmittel zu deinem Digitalen Kühlschrank hinzu. "
"Wir werden dich daran erinnen, es rechtzeitig zu benutzen und dir so helfen keine Lebensmittel mehr zu verschwenden. "
"#StopFoodwaste ")
    st.sidebar.image('18-04-_2024_11-16-47.png', use_column_width=True)
    st.sidebar.title("")
    if st.sidebar.button("Mein Kühlschrank"):
        show_my_fridge()
    if st.sidebar.button("Neues Lebensmittel hinzufügen"):
        add_food_to_fridge()
    st.sidebar.markdown("---")  # Separator
    if st.sidebar.button("Freunde einladen"):
        show_my_friends()
    if st.sidebar.button("Einstellungen"):
        show_settings()

def show_my_fridge():
    """Display the contents of the fridge."""
    st.title("Mein Kühlschrank")
    init_dataframe_food()  # Daten laden
    if not st.session_state.df_food.empty:
        st.dataframe(st.session_state.df_food)
    else:
        st.write("Der Kühlschrank ist leer.")


def add_food_to_fridge():
    """Add a new food item to the fridge."""
    st.title("Neues Lebensmittel hinzufügen")
    with st.form("new_food_form"):
        st.write("Füllen Sie die folgenden Felder aus:")
        food_name = st.text_input("Lebensmittel")
        category = st.selectbox("Kategorie", ["Bitte wählen","Gemüse", "Obst", "Milchprodukte", "Fleisch", "Fisch", "Eier", "Getränke", "Saucen", "Getreideprodukte", "Tiefkühlprodukte"])
        location = st.selectbox("Lagerort", ["Bitte wählen","Schrank", "Kühlschrank", "Tiefkühler", "offen"])
        area = st.selectbox("Standort", ["Bitte wählen", "Mein Kühlschrank", "geteilter Kühlschrank"])
        expiry_date = st.date_input("Ablaufdatum")
        submitted = st.button("Hinzufügen")
        if submitted:
            new_entry_food = pd.DataFrame([[food_name, category, location, area, expiry_date]], columns=DATA_COLUMNS_FOOD)
            st.session_state.df_food = pd.concat([st.session_state.df_food, new_entry_food], ignore_index=True)
            st.dataframe(st.session_state.df_food)
            st.session_state.github.write_df(DATA_FILE_FOOD, st.session_state.df_food, "Updated fridge contents")
            st.success("Lebensmittel erfolgreich hinzugefügt!")
            show_my_fridge()




def show_my_friends():
    st.write("Meine Freunde")

def show_settings():
    st.write("Einstellungen")

def save_data_to_database_login():
    st.session_state.github.write_df(DATA_FILE, st.session_state.df_login, "Updated registration data")

def save_data_to_database_food():
    if 'github' in st.session_state:
        st.session_state.github.write_df(DATA_FILE_FOOD, st.session_state.df_food, "Updated food data")

def main():
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
