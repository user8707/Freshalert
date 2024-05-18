import binascii 
import streamlit as st
import pandas as pd
import bcrypt
from github_contents import GithubContents
from PIL import Image
from datetime import datetime, timedelta
import random
import string
import time

# Konstante für das Login
DATA_FILE = "FreshAlert-Registration.csv"
DATA_COLUMNS = ["Vorname", "Nachname", "E-Mail", "Passwort", "Passwort wiederholen", "User ID"]  

# Konstante für das Datenrepo von meinem Kühlschrank
DATA_FILE_FOOD = "Kühlschrankinhalt.csv"
DATA_COLUMNS_FOOD = ["User ID", "Lebensmittel", "Kategorie", "Lagerort", "Standort", "Ablaufdatum"] 

# Konstante für das  Datenrepo für den geteilten Kühlschrank
DATA_FILE_SHARED_FRIDGE = "geteilte_kuehlschraenke.csv"
DATA_COLUMNS_SHARED_FRIDGE = ["Kuehlschrank_ID", "User ID", "Lebensmittel", "Kategorie", "Lagerort", "Standort", "Ablaufdatum", "Tage_bis_Ablauf", "Benutzername"]

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
    if st.button("🔓 Login"):
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
        if st.button("🆕 Neu Registrieren", key="registration_button"):
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
    navigation = st.sidebar.radio("Navigation", ["🏠 Startbildschirm", "🗄️ Mein Kühlschrank", "🤝 Geteilter Kühlschrank", "🛒 Neues Lebensmittel hinzufügen", "📧 Freunde einladen","ℹ️ Information", "⚙️ Einstellungen", "🔐 Ausloggen"])

    # Check which page to display
    if navigation == "🏠 Startbildschirm":
        show_mainpage()
    elif navigation == "🗄️ Mein Kühlschrank":
        show_my_fridge_page()
    elif navigation == "🤝 Geteilter Kühlschrank":
        show_shared_fridge_page()
    elif navigation == "🛒 Neues Lebensmittel hinzufügen":
        add_food_to_fridge()
    elif navigation == "📧 Freunde einladen":
        show_my_friends()
    elif navigation == "ℹ️ Information":
        show_informations()
    elif navigation == "⚙️ Einstellungen":
        show_settings()
    elif navigation == "🔐 Ausloggen":
        logout()
        
def generate_new_fridge_id():
    # Generate a random 6-digit fridge ID
    return ''.join(random.choices(string.digits, k=6))


def show_expired_food_on_mainpage():
    # Filtern aller Lebensmittel des aktuellen Benutzers, die bald ablaufen
    user_expired_food = st.session_state.df_food[(st.session_state.df_food['User ID'] == st.session_state.user_id) & (st.session_state.df_food['Tage_bis_Ablauf'] <= 1)]

    if not user_expired_food.empty:
        st.markdown("---")
        st.header("Deine Lebensmittel, welche bald ablaufen⚠️:")
        st.subheader("In meinem Kühlschrank")
        for index, row in user_expired_food.iterrows():
            st.error(f"**{row['Lebensmittel']}** (Ablaufdatum: {row['Ablaufdatum']}, Lagerort: {row['Lagerort']})")

def show_expired_food_shared_fridge():
    # Filtern aller Lebensmittel im geteilten Kühlschrank, die bald ablaufen
    shared_fridge_expired_food = st.session_state.df_shared_fridge[(st.session_state.df_shared_fridge['Tage_bis_Ablauf'] <= 1)]

    if not shared_fridge_expired_food.empty:
        st.markdown(" --- ")
        st.subheader("In deinem geteilten Kühlschränken")
        for index, row in shared_fridge_expired_food.iterrows():
            st.error(f"**{row['Lebensmittel']}** (Ablaufdatum: {row['Ablaufdatum']}, Lagerort: {row['Lagerort']}, Kühlschrank: {row['Benutzername']})")
            


def show_mainpage():
    st.title("FreshAlert")
    st.subheader("Herzlich Willkommen bei FreshAlert. Deine App für deine Lebensmittel! ")            
    st.write("Füge links deine ersten Lebensmittel zu deinem Digitalen Kühlschrank hinzu. "
                 "Wir werden dich daran erinnern, es rechtzeitig zu benutzen und dir so helfen, keine Lebensmittel mehr zu verschwenden. "
                 "#StopFoodwaste ")
    #Zeigt die bald ablaufenden Lebensmittel an
    show_expired_food_on_mainpage()
    show_expired_food_shared_fridge()

def colorize_expiring_food(df):
    def colorize(val):
        if val <= 0:
            return 'color: red; font-weight: bold; font-size: 14px'
        elif val == 1:
            return 'color: orange; font-weight: bold; font-size: 14px'
        else:
            return 'color: green; font-weight: bold; font-size: 14px'
    
    # Convert 'Ablaufdatum' column to datetime with error handling
    df['Ablaufdatum'] = pd.to_datetime(df['Ablaufdatum'], errors='coerce')
    
    # Calculate days until expiration date
    df['Tage_bis_Ablauf'] = (df['Ablaufdatum'] - pd.Timestamp.now() - timedelta(days=-1)).dt.days
    
    # Apply colorization to table columns and format numbers
    df_styled = df.style.applymap(colorize, subset=['Tage_bis_Ablauf']).format({'Tage_bis_Ablauf': '{:.0f}'})
    
    return df_styled

def show_fridge_items(user_id):
    # Load fridge items for the given user_id
    fridge_items = load_fridge_items(user_id)
    
    # Set a custom index for the DataFrame
    fridge_items.index = [f"Item {i+1}" for i in range(len(fridge_items))]
    
    # Display the fridge items without the index column
    st.write(fridge_items.to_string(index=False))

def show_my_fridge_page():
    st.title("Meine Vorräte")
    init_dataframe_food()  # Daten laden
    
    if not st.session_state.df_food.empty:
        # Filtere die Einträge nach der User ID
        user_fridge = st.session_state.df_food[st.session_state.df_food['User ID'] == st.session_state.user_id]
        
        if not user_fridge.empty:
            # Sortiere das DataFrame nach den Tagen bis zum Ablaufdatum
            user_fridge = user_fridge.sort_values(by='Tage_bis_Ablauf', ascending=True)
            
             # Zeige nur die gewünschten Spalten an
            user_fridge_display = user_fridge[['Lebensmittel', 'Kategorie', 'Lagerort', 'Standort','Ablaufdatum', 'Tage_bis_Ablauf']]
            
            # Colorize the expiring food entries
            df_styled = colorize_expiring_food(user_fridge_display)
                               
            st.write(df_styled)

            # Allow the user to delete a food entry
            food_names = user_fridge_display['Lebensmittel'].tolist()
            food_index_to_delete = st.selectbox("Lebensmittel auswählen", food_names, index=0)
            if st.button("🚮 Lebensmittel löschen", key="delete_entry_button"):
                index_to_delete = user_fridge_display[user_fridge_display['Lebensmittel'] == food_index_to_delete].index
                st.session_state.df_food.drop(index=index_to_delete, inplace=True)
                save_data_to_database_food()  # Save the updated dataframe
                st.experimental_rerun()  # Rerun the app to refresh the page
                st.success("Eintrag erfolgreich gelöscht!")
                
        else:
            st.write("Der Kühlschrank ist leer oder Sie haben keine Einträge.")
    else:
        st.write("Der Kühlschrank ist leer.")
        
def show_shared_fridge_page():
    st.title("Geteilter Kühlschrank")

    if st.button("Neuen geteilten Kühlschrank erstellen"):
        st.session_state.create_new_fridge = True

    if st.session_state.get("create_new_fridge"):
        # Benutzereingabe für den Namen des neuen geteilten Kühlschranks
        new_fridge_name = st.text_input("Name des neuen geteilten Kühlschranks")
        if new_fridge_name:
            st.session_state.new_fridge_name = new_fridge_name

        # Button zum Erstellen des Kühlschranks und Generieren des Codes
        if st.button("Kühlschrank erstellen und Code generieren"):
            new_fridge_name = st.session_state.get("new_fridge_name")
            new_fridge_id = generate_new_fridge_id()
            st.session_state.shared_fridge_id = new_fridge_id
            st.session_state.create_new_fridge = False
            st.success(f"Neuer geteilter Kühlschrank '{new_fridge_name}' erfolgreich erstellt! Kühlschrank-ID: {new_fridge_id}")
            
            # Neue Zeile im Datenrepository hinzufügen
            if st.session_state.user_logged_in:
                new_fridge_data = {
                    "Kuehlschrank_ID": new_fridge_id,
                    "User ID": st.session_state.user_id,
                    "Benutzername": new_fridge_name  # Hinzufügen des Benutzernamens für den Kühlschrank
                }
                st.session_state.df_shared_fridge = pd.concat([st.session_state.df_shared_fridge, pd.DataFrame([new_fridge_data])], ignore_index=True)
                save_data_to_database_shared_fridge()
            
            # Automatisch die Seite neu laden
            st.experimental_rerun()

    if st.session_state.user_logged_in:
        user_fridges = st.session_state.df_shared_fridge[st.session_state.df_shared_fridge['User ID'] == st.session_state.user_id]
        if not user_fridges.empty:
            fridge_names = user_fridges['Benutzername'].unique().tolist()
            selected_fridge_name = st.selectbox("Wählen Sie einen geteilten Kühlschrank aus:", fridge_names)
            
            if selected_fridge_name:
                selected_fridge_id = user_fridges.loc[user_fridges['Benutzername'] == selected_fridge_name, 'Kuehlschrank_ID'].iloc[0]
                show_selected_fridge(selected_fridge_id)
        else:
            st.write("Sie haben keinen geteilten Kühlschrank.")
    else:
        st.write("Sie müssen angemeldet sein, um geteilte Kühlschränke anzuzeigen.")


def show_selected_fridge(fridge_id):
    st.subheader(f"Geteilter Kühlschrank ID: {fridge_id}")

    # Filter the shared fridge DataFrame based on the selected fridge_id
    fridge_items = st.session_state.df_shared_fridge[st.session_state.df_shared_fridge['Kuehlschrank_ID'] == fridge_id]

    if not fridge_items.empty:
        # Filter items where Standort is not empty
        fridge_items = fridge_items[fridge_items['Standort'].notna()]

        if not fridge_items.empty:
            # Sort the DataFrame by expiration date
            fridge_items = fridge_items.sort_values(by='Tage_bis_Ablauf', ascending=True)
            
            # Display the fridge items
            fridge_items_display = fridge_items[['Lebensmittel', 'Kategorie', 'Lagerort', 'Standort', 'Ablaufdatum', 'Tage_bis_Ablauf']]
            df_styled = colorize_expiring_food(fridge_items_display)
            st.write(df_styled)

            # Allow the user to delete a food entry
            food_names = fridge_items_display['Lebensmittel'].tolist()
            food_index_to_delete = st.selectbox("Lebensmittel auswählen, um zu löschen:", food_names, index=0)
            if st.button("🚮 Lebensmittel löschen", key="delete_food_button"):
                index_to_delete = fridge_items_display[fridge_items_display['Lebensmittel'] == food_index_to_delete].index
                st.session_state.df_shared_fridge.drop(index=index_to_delete, inplace=True)
                save_data_to_database_shared_fridge()  # Save the updated dataframe
                st.success("Lebensmittel erfolgreich gelöscht!")
                st.experimental_rerun()  # Rerun the app to refresh the page
        else:
            st.write("Keine Lebensmitteleinträge vorhanden, die einen Standort haben.")
    else:
        st.write("Dieser Kühlschrank ist leer oder enthält keine Standortinformationen.")

def add_food_to_fridge():
    st.title("Neues Lebensmittel hinzufügen")
           
    new_entry = {
        DATA_COLUMNS_FOOD[0]: st.session_state.user_id,  # Setze die User ID als UserID
        DATA_COLUMNS_FOOD[1]: st.text_input(DATA_COLUMNS_FOOD[1]), #Lebensmittel
        DATA_COLUMNS_FOOD[2]: st.selectbox("Kategorie", ["Bitte wählen",  "🥦 Gemüse", "🍎 Obst", "🥛 Milchprodukte", "🍗 Fleisch", "🐟 Fisch", "🍳 Eier", "🍺 Getränke", "🥫 Saucen", "🥯 Getreideprodukte", "🍨 Tiefkühlprodukte", "🧁 Gebäcke", "🍕 Sonstiges"]), #Kategorie
        DATA_COLUMNS_FOOD[3]: st.selectbox("Lagerort", ["Bitte wählen", "📦Schrank", "🗄️Kühlschrank", "🧊Tiefkühler", "offen"]), # Location
        DATA_COLUMNS_FOOD[4]: st.selectbox("Standort", ["Bitte wählen", "🗄️Mein Kühlschrank", "🤝geteilter Kühlschrank"]), #area
        DATA_COLUMNS_FOOD[5]: st.date_input("Ablaufdatum"), #Ablaufdatum
    }

    # Überprüfe, ob die Pflichtfelder ausgefüllt sind
    if not new_entry[DATA_COLUMNS_FOOD[1]] or new_entry[DATA_COLUMNS_FOOD[4]] == "Bitte wählen" or not new_entry[DATA_COLUMNS_FOOD[5]]:
        st.error("Bitte fülle die Pflichtfelder (Lebensmittel, Standort, Ablaufdatum) aus.")
        return
        
    # Überprüfe, ob das Ablaufdatum gültig ist
    if 'Ablaufdatum' in new_entry and new_entry['Ablaufdatum'] < datetime.now().date():
        st.error("Das Ablaufdatum muss in der Zukunft liegen.")
        return

    # Berechne die Tage bis zum Ablaufdatum
    if 'Ablaufdatum' in new_entry:
        days_until_expiry = (new_entry['Ablaufdatum'] - datetime.now().date()).days
    else:
        days_until_expiry = None

    # Füge die Tage_bis_Ablauf-Spalte zum neuen Eintrag hinzu
    new_entry['Tage_bis_Ablauf'] = days_until_expiry

    for key, value in new_entry.items():
        if value == "":
            st.error(f"Bitte ergänze das Feld '{key}'")
            return
    
    if new_entry["Standort"] == "🤝geteilter Kühlschrank":
        if "shared_fridge_id" not in st.session_state:
            st.error("Bevor du ein Lebensmittel zum geteilten Kühlschrank hinzufügen kannst, musst du zuerst einen geteilten Kühlschrank erstellen.")
            return
        else:
            # Holen Sie sich alle verfügbaren geteilten Kühlschrank-Namen
            shared_fridge_options = st.session_state.df_shared_fridge["Benutzername"].unique().tolist()
            selected_shared_fridge_name = st.selectbox("Wählen Sie den geteilten Kühlschrank aus:",shared_fridge_options)

            # Überprüfen Sie, ob eine Auswahl getroffen wurde
            if selected_shared_fridge_name:
                # Holen Sie sich die entsprechende Kühlschrank-ID basierend auf dem ausgewählten Namen
                selected_shared_fridge_id = st.session_state.df_shared_fridge.loc[st.session_state.df_shared_fridge["Benutzername"] == selected_shared_fridge_name, "Kuehlschrank_ID"].iloc[0]
                # Setzen Sie die ausgewählte Kühlschrank-ID im neuen Eintrag
                new_entry["Kuehlschrank_ID"] = selected_shared_fridge_id
                st.session_state.df_shared_fridge = pd.concat([st.session_state.df_shared_fridge, pd.DataFrame([new_entry])], ignore_index=True)
                save_data_to_database_shared_fridge()
            else:
                st.error("Bitte wählen Sie einen geteilten Kühlschrank aus.")
                return
    elif new_entry["Standort"] == "🗄️Mein Kühlschrank":
        st.session_state.df_food = pd.concat([st.session_state.df_food, pd.DataFrame([new_entry])],ignore_index=True)
        save_data_to_database_food()
    else:
        st.error("Ungültiger Standort ausgewählt.")
        return

    st.success("Lebensmittel erfolgreich hinzugefügt!")


def show_settings():
    st.title("Einstellungen")
    
    # Get the user's shared fridges
    if st.session_state.user_logged_in:
        user_shared_fridges = st.session_state.df_shared_fridge[st.session_state.df_shared_fridge['User ID'] == st.session_state.user_id]
        
        if not user_shared_fridges.empty:
            fridge_names = user_shared_fridges['Benutzername'].unique().tolist()  # Get unique fridge names
            selected_fridge_name_to_delete = st.selectbox("Wählen Sie einen geteilten Kühlschrank zum Löschen aus:", fridge_names)
            selected_fridge_id_to_delete = user_shared_fridges.loc[user_shared_fridges['Benutzername'] == selected_fridge_name_to_delete, 'Kuehlschrank_ID'].iloc[0]
            
            if st.button("🚮Geteilten Kühlschrank löschen"):
                # Lösche den ausgewählten geteilten Kühlschrank
                st.session_state.df_shared_fridge = st.session_state.df_shared_fridge[st.session_state.df_shared_fridge['Kuehlschrank_ID'] != selected_fridge_id_to_delete]
                save_data_to_database_shared_fridge()
                st.success(f"Geteilter Kühlschrank mit dem Namen '{selected_fridge_name_to_delete}' erfolgreich gelöscht!")
                #für eine Verzögerung der Aktualisierung
                time.sleep(2)
                
                st.experimental_rerun()
        else:
            st.write("Sie haben keinen geteilten Kühlschrank.")
    else:
        st.write("Sie müssen angemeldet sein, um Ihre geteilten Kühlschränke zu verwalten.")
        
        # Show success message if fridge_deleted flag is set
    if 'fridge_deleted' in st.session_state and st.session_state.fridge_deleted:
        st.success("Der Kühlschrank wurde erfolgreich gelöscht.")
        st.session_state.fridge_deleted = False  # Reset the flag


def show_my_friends():
    st.title("Zeige deinen Freunden wie sie ihre Vorräte am besten organsieren können")
    st.write("Teile die App FreshAltert in dem du ihnen den Link unserer App schickst https://fresh-alert.streamlit.app/")
    
    friend_code = st.text_input("Freundecode eingeben")
    if st.button("Freundecode hinzufügen"):
        if friend_code in st.session_state.df_shared_fridge['Kuehlschrank_ID'].values:
            st.session_state.shared_fridge_id = friend_code
            st.success("Freundecode erfolgreich hinzugefügt!")
        else:
            st.error("Ungültiger Freundecode.")


    
    st.write("Wir als Entwickler-Team würden uns riesig freuen")
    st.write("Liebe Grüsse von Mirco, Sarah und Sebastian, welche die App mit viel Liebe und noch mehr Schweiss und Tränen entwickelt haben")

def show_informations():
    st.title("Was ist Foodwaste?")
    st.image("images/Foodwaste1.png", width=650)  # Ändere die Breite auf 150 Pixel und die Höhe auf 200 Pixel
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

    st.image ("images/Foodwaste2.png", width=650)
    st.image ("images/Foodwaste3.png", width=650)

    st.title("5 Einfache Tipps")
    st.subheader("**1. Clever Einkaufen - nur so viel wie man braucht**")
    st.write("Plane deinen Wochenbedarf und erstelle eine Einkaufsliste. Bevor du einkaufen gehst, wirf einen Blick in den Kühlschrank, um zu sehen, was noch da ist.")
    st.write("Kaufe nur, was du brauchst. Gib kleinen oder unverpackten Portionen den Vorzug und sei vorsichtig mit Aktionen – nur kaufen, wenn du sie auch wirklich konsumieren wirst.")
    st.write("Kaufe, wenn immer möglich, lokal und saisonal.")
    st.write("Iss etwas Kleines vor dem Einkauf – ein knurrender Magen wird dich dazu verleiten, mehr zu kaufen, als du brauchst!")
    
    st.subheader("**2. Optimal Lagern - verlängere die Haltbarkeit deiner Lebensmittel**")
    st.write("„Zu verbrauchen bis“, „Zu verkaufen bis“ und „Mindestens haltbar bis“ haben unterschiedliche Bedeutungen! Wenn das Datum „zu verbrauchen bis“ überschritten wurde, solltest du die Lebensmittel nicht mehr konsumieren. Ansonsten gilt: Orientiere dich nicht nur an den Daten, sondern vertraue auf deine Sinne – sehen, riechen, schmecken – um herauszufinden, ob die Lebensmittel noch genießbar sind.")
    st.write("Stelle die Temperatur deines Kühlschranks auf 5ºC ein – bei wärmeren Temperaturen wird das Wachstum schädlicher Bakterien begünstigt.")
    st.write("Bewahre Essensreste in durchsichtigen Behältern auf. Platziere sie so, dass du sie nicht vergisst, und konsumiere sie innerhalb von 1 bis 3 Tagen.")
    st.write("Hast du zu viel eingekauft und kannst nicht alles davon essen? Die meisten Lebensmittel können eingefroren werden! Brot bis zu drei Monaten, gewisse tierische Produkte bis zu einem Jahr! Achte bei tierischen Produkten darauf, dass die Kühlkette nicht unterbrochen wird.")
    st.write("Organisiere dich gut – verwende das first-in-first-out-Prinzip für verderbliche Lebensmittel wie Früchte und Gemüse: Ältere Produkte kommen nach vorne, was neu in den Kühlschrank kommt, geht nach hinten.")

    st.subheader("**3. Richtig Portionieren - kleinere Mengen kochen und servieren**")
    st.write("Hier eine Kartoffel zu viel, dort ein kleiner Rest Pasta im Topf – häufig sind es kleine Portionen, die übrig bleiben und dann entsorgt werden. Der beste Trick, dies zu umgehen: Schon vor dem Kochen richtig portionieren!")
    st.write("Serviere kleinere Portionen und schöpfe nach, falls du noch immer hungrig bist.")
    st.write("Wenn dennoch etwas übrig bleibt: Richtig lagern, dann kannst du es zu einem späteren Zeitpunkt genießen oder daraus ein neues Menü zaubern. Oder nimm die Reste deines Abendessens am nächsten Tag mit zur Arbeit.")

    st.subheader("**4. Spaß am Kochen - mit einfachen und kreativen Ideen**")
    st.write("Weißt du nicht, was du kochen sollst? Viele Rezeptideen findest du online. Fehlt dir für dein Rezept eine Zutat? Bestimmt lässt es sich umwandeln – lass deiner Kreativität freien Lauf!")
    st.write("Widme einen Tag pro Woche der Resteverwertung, z.B. den Montag, wenn du Reste hast vom Wochenende und keine Lust, lange in der Küche zu stehen.")
    st.write("Keine Lust, nochmals die gleichen Reste zu essen? Verwandle die Reste in ein neues Menü – hast du zum Beispiel schon einmal daran gedacht, aus Kräuterresten ein leckeres Pesto zu zaubern?")

    st.subheader("**5. Gemeinsam genießen - weil du dein Essen liebst**")
    st.write("Teile deine Liebe zum Essen mit Freunden und Familie, damit die Reduktion von Food Waste auch in deinem Umfeld zur Ehrensache wird.")
    st.write("Zu viel Essen im Haus? Verschenke es an Freunde oder Nachbarn oder bringe die noch verpackten Lebensmittel zu einem öffentlichen Kühlschrank.")
    st.write("Kenne deine Lebensmittel – und wie du sie am besten lagerst, portionierst und zubereitest. Nützliche Tipps findest du unter foodwaste.ch.")

    st.title("Quellen")
    st.write("https://foodwaste.ch/was-ist-food-waste/")
    st.write("https://foodwaste.ch/was-ist-food-waste/5-schritte/")

def logout():
    st.session_state.user_logged_in = False
    st.success("Erfolgreich ausgeloggt!")
    st.session_state.current_user_id = None
    st.experimental_rerun()  # Rerun the app to go back to the login page


def save_data_to_database_login():
    if 'github' in st.session_state:
        st.session_state.github.write_df(DATA_FILE, st.session_state.df_login, "Updated registration data")

def save_data_to_database_food():
    if 'github' in st.session_state:
        st.session_state.github.write_df(DATA_FILE_FOOD, st.session_state.df_food, "Updated food data")

def save_data_to_database_shared_fridge():
    if 'github' in st.session_state:
        st.session_state.github.write_df(DATA_FILE_SHARED_FRIDGE, st.session_state.df_shared_fridge, "Updated shared fridge data")


def main():
    init_github()
    init_dataframe_login()
    init_dataframe_food()
    init_dataframe_shared_fridge()
    if 'user_logged_in' not in st.session_state:
        st.session_state.user_logged_in = False

    if not st.session_state.user_logged_in:
        show_login_page()
    else:
        show_fresh_alert_page()

if __name__ == "__main__":
    main()
