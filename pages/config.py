# config.py
DATA_FILE = "FreshAlert-Registration.csv"
DATA_COLUMNS = ["Vorname", "Nachname", "E-Mail", "Passwort", "Passwort wiederholen"]
DATA_FILE_FOOD = "Kühlschrankinhalt.csv"
DATA_COLUMNS_FOOD = ["Lebensmittel", "Kategorie", "Lagerort", "Ablaufdatum", "Standort"]

# Set page configuration
st.set_page_config(
    page_title="FreshAlert",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded"
)
