import streamlit as st
import pandas as pd
from github_contents import GithubContents
from PIL import Image
import bcrypt  # Importiere die bcrypt-Bibliothek

# Set constants for user registration
DATA_FILE = "FreshAlert-Registration.csv"
DATA_COLUMNS = ["Vorname", "Nachname", "E-Mail", "Passwort", "UserID"]  # Neue Spalte für die User-ID hinzugefügt

# Set constants for fridge contents
DATA_FILE_FOOD = "Kühlschrankinhalt.csv"
DATA_COLUMNS_FOOD = ["UserID", "Lebensmittel", "Kategorie", "Lagerort", "Standort", "Ablaufdatum"]  # Neue Spalte für die User-ID hinzugefügt

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
                st.session_state.current_user_id = row["UserID"]  # Speichere die User-ID in der Session
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
                # Generiere eine eindeutige User-ID für den neuen Benutzer
                user_id = bcrypt.hashpw(new_entry["E-Mail"].encode('utf-8'), bcrypt.gensalt())
                new_entry["UserID"] = user_id.decode('utf-8')
                
                # Hash the password before storing it
                hashed_password = bcrypt.hashpw(new_entry["Passwort"].encode('utf-8'), bcrypt.gensalt())
                new_entry["Passwort"] = hashed_password.decode('utf-8')
                
                new_entry_df = pd.DataFrame([new_entry])
                st.session_state.df_login = pd.concat([st.session_state.df_login, new_entry_df], ignore_index=True)
                save_data_to_database_login()
                st.success("Registrierung erfolgreich!")
                st.session_state.show_registration = False  # Reset status
            else:
                st.error("Die Passwörter stimmen nicht überein.")

def show_fresh_alert_page():
    col1, col2 = st.columns([7, 1])
    col2.image(small_image, use_column_width=False, clamp=True)
    st.title("FreshAlert")
    
    st.sidebar.image('images/18-04-_2024_11-16-47-Photoroom.png-Photoroom.png', use_column_width=True)

    # Create buttons for navigation
    navigation = st.sidebar.radio("Navigation", ["Startbildschirm", "Mein Kühlschrank", "Neues Lebensmittel hinzufügen", "Freunde einladen","Information", "Einstellungen", "Ausloggen"])

    # Check which page to display
    if navigation == "Startbildschirm":
        show_mainpage()
    elif navigation == "Mein Kühlschrank":
        show_my_fridge_page()
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

def show_expired_food_on_mainpage():
    # Filtern aller Lebensmittel, die rot markiert sind (Ablaufdatum erreicht oder überschritten)
    expired_food = st.session_state.df_food[st.session_state.df_food['Tage_bis_Ablauf'] <= 1]

    if not expired_food.empty:
        st.markdown("---")
        st.subheader("Deine Lebensmittel, welche bald ablaufen!:")
        for index, row in expired_food.iterrows():
            st.error(f"**{row['Lebensmittel']}** (Ablaufdatum: {row['Ablaufdatum']}, Lagerort: {row['Lagerort']})")

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
        # Filtere die Einträge basierend auf der aktuellen User-ID
        user_fridge = st.session_state.df_food[st.session_state.df_food['UserID'] == st.session_state.current_user_id]
        
        if not user_fridge.empty:
            # Sortiere das DataFrame nach den Tagen bis zum Ablaufdatum
            user_fridge = user_fridge.sort_values(by='Tage_bis_Ablauf', ascending=True)
            
            # Colorize the expiring food entries
            df_styled = colorize_expiring_food(user_fridge)
            
            # Display the formatted DataFrame
            st.write(df_styled)
            
            # Allow the user to delete a food entry
            index_to_delete = st.number_input("Index des zu löschenden Eintrags", min_value=0, max_value=len(user_fridge)-1, step=1)
            if st.button("Eintrag löschen", key="delete_entry_button"):
                user_fridge.drop(index=user_fridge.index[index_to_delete], inplace=True)
                save_data_to_database_food()  # Save the updated dataframe
                st.success("Eintrag erfolgreich gelöscht!")
        else:
            st.write("Der Kühlschrank ist leer für diesen Benutzer.")
    else:
        st.write("Der Kühlschrank ist leer.")

def add_food_to_fridge():
    st.title("Neues Lebensmittel hinzufügen")
    
    # Erstelle ein neues DataFrame mit der User-ID
    new_entry = {
        "UserID": st.session_state.current_user_id,  # Füge die aktuelle User-ID hinzu
        DATA_COLUMNS_FOOD[1]: st.text_input(DATA_COLUMNS_FOOD[1]), #Lebensmittel
        DATA_COLUMNS_FOOD[2]: st.selectbox("Kategorie", ["Bitte wählen","Gemüse", "Obst", "Milchprodukte", "Fleisch", "Fisch", "Eier", "Getränke", "Saucen", "Getreideprodukte", "Tiefkühlprodukte", "Gebäcke", "Sonstiges"]), #Kategorie
        DATA_COLUMNS_FOOD[3]: st.selectbox("Lagerort", ["Bitte wählen", "Schrank", "Kühlschrank", "Tiefkühler", "offen"]), # Location
        DATA_COLUMNS_FOOD[4]: st.selectbox("Standort", ["Bitte wählen", "Mein Kühlschrank", "geteilter Kühlschrank"]), #area
        DATA_COLUMNS_FOOD[5]: st.date_input("Ablaufdatum"), #Ablaufdatum
    }

    for key, value in new_entry.items():
        if value == "" or value is None:
            st.error(f"Bitte ergänze das Feld '{key}'")
            return

    if st.button("Hinzufügen"):
        new_entry_df = pd.DataFrame([new_entry])
        st.session_state.df_food = pd.concat([st.session_state.df_food, new_entry_df], ignore_index=True)
        save_data_to_database_food()
        st.success("Lebensmittel erfolgreich hinzugefügt!")

def save_data_to_database_food():
    if 'github' in st.session_state:
        st.session_state.github.write_df(DATA_FILE_FOOD, st.session_state.df_food, "Updated food data")

def show_settings():
    st.title("Einstellungen")

def show_my_friends():
    st.title("Zeige deinen Freunden wie sie ihre Vorräte am besten organsieren können")
    st.write("Teile die App FreshAltert in dem du ihnen den Link unserer App schickst https://fresh-alert.streamlit.app/")
    st.write("Wir als Entwickler-Team würden uns riesig freuen")
    st.write("Liebe Grüsse von Mirco, Sarah und Sebastian, welche die App mit viel Liebe und noch mehr Schweiss und Tränen entwickelt haben")

def show_informations():
    st.title("Was ist Foodwaste?")
    st.image ("images/Foodwaste1.png")
    st.title("Tipps zur Reduzierung von Food Waste")
    st.header("Wo geschieht Foodwaste?")
    st.write("Die Gastronomie und die Haushalte verursachen zusammen 35% der Lebensmittelabfälle.")
    st.write("In den Haushalten entsteht Food Waste zum Beispiel, weil:")
    st.write("- wir mehr kaufen, als wir benötigen.")
    st.write("- wir größere Verpackungen kaufen, als wir brauchen.")
    st.write("- wir Lebensmittel im Kühlschrank vergessen.")
    st.write("- wir Lebensmittel nicht korrekt lagern und sich so die Haltbarkeit verringert.")
    st.write("- wir das Mindesthaltbarkeitsdatum falsch interpretieren und Produkte nicht mit unseren Sinnen beurteilen.")
    st.write("- wir mehr kochen, als wir brauchen und Reste nicht verwerten.")

    st.image ("images/Foodwaste2.png")
    
    st.header("Wie können wir Lebensmittelverschwendung reduzieren?")
    st.write("1. Einkaufsliste schreiben:")
    st.write("Überlege dir vor dem Einkaufen, was du tatsächlich benötigst. Plane die Mahlzeiten und schreibe eine Einkaufsliste. So kaufst du weniger ein und sparst Geld.")
    st.write("2. Richtig lagern:")
    st.write("Achte darauf, Lebensmittel richtig zu lagern. Dies erhöht ihre Haltbarkeit. Einige Lebensmittel verderben schneller, wenn sie im Kühlschrank lagern, während sie andere vor der Reifung schützen.")
    st.write("3. Lebensmittelreste verwerten:")
    st.write("Koche Reste von Lebensmitteln und variiere das Gericht, indem du beispielsweise Gemüsereste in Suppen oder Smoothies verwendest.")
    st.write("4. Aufmerksam einkaufen:")
    st.write("Achte beim Einkauf auf das Mindesthaltbarkeitsdatum. Produkte, die kurz vor Ablauf des Mindesthaltbarkeitsdatums stehen, sollten zeitnah verzehrt werden.")
    st.write("5. Portionen richtig kalkulieren:")
    st.write("Koche nur so viel, wie du essen kannst. Überlege dir vor dem Kochen, wie viele Portionen du benötigst und passe die Mengen entsprechend an.")
    st.write("6. Kreative Rezepte ausprobieren:")
    st.write("Probiere neue Rezepte aus, um übrig gebliebene Zutaten zu verwenden. Es gibt viele kreative Rezepte, die Reste zu leckeren Gerichten verwandeln.")

def save_data_to_database_login():
    if 'github' in st.session_state:
        st.session_state.github.write_df(DATA_FILE, st.session_state.df_login, "Updated login data")

def logout():
    st.session_state.user_logged_in = False
    st.session_state.current_user_id = None

def main():
    init_github()
    if st.session_state.get("user_logged_in", False):
        show_fresh_alert_page()
    else:
        show_login_page()

main()
