import streamlit as st
import pandas as pd
from github_contents import GithubContents

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

def init_dataframe_food():
    """Initialize or load the dataframe for fridge contents."""
    if 'df_food' not in st.session_state:
        if st.session_state.github.file_exists(DATA_FILE_FOOD):
            st.session_state.df_food = st.session_state.github.read_df(DATA_FILE_FOOD)
        else:
            st.session_state.df_food = pd.DataFrame(columns=DATA_COLUMNS_FOOD)


def show_my_fridge_page():
    """Display the contents of the fridge."""
    st.title("Mein Kühlschrank")
    init_dataframe_food()  # Daten laden
    
    if not st.session_state.df_food.empty:
        st.dataframe(st.session_state.df_food)
    else:
        st.write("Der Kühlschrank ist leer.")


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

def show_fresh_alert_page():
    st.title("FreshAlert")
    st.subheader("Herzlich Willkommen bei FreshAlert. Deine App für deine Lebensmittel! "            
"Füge links deine ersten Lebensmittel zu deinem Digitalen Kühlschrank hinzu. "
"Wir werden dich daran erinnen, es rechtzeitig zu benutzen und dir so helfen keine Lebensmittel mehr zu verschwenden. "
"#StopFoodwaste ")
    st.sidebar.image('18-04-_2024_11-16-47.png', use_column_width=True)
    st.sidebar.title("")
    if st.sidebar.button("Mein Kühlschrank"):
        show_my_fridge_page()
    if st.sidebar.button("Neues Lebensmittel hinzufügen"):
        add_food_to_fridge()
    st.sidebar.markdown("---")  # Separator
    if st.sidebar.button("Freunde einladen"):
        show_my_friends()
    if st.sidebar.button("Einstellungen"):
        show_settings()



def add_food_to_fridge():
    st.title("Neues Lebensmittel hinzufügen")
    init_dataframe_food()  # Daten laden

    food_name = st.text_input("Lebensmittel")
    category = st.selectbox("Kategorie", ["Gemüse", "Obst", "Milchprodukte", "Fleisch", "Fisch", "Eier", "Getränke", "Saucen", "Getreideprodukte", "Tiefkühlprodukte"])
    location = st.selectbox("Lagerort", ["Schrank", "Kühlschrank", "Tiefkühler", "offen"])
    area = st.selectbox("Standort", ["Mein Kühlschrank", "geteilter Kühlschrank"])
    expiry_date = st.date_input("Ablaufdatum")

    if st.button("Lebensmittel hinzufügen"):
        if food_name and category and location and area and expiry_date:
            new_entry_food = pd.DataFrame([[food_name, category, location, expiry_date, area]], columns=DATA_COLUMNS_FOOD)
            new_df = pd.concat([st.session_state.df_food, new_entry_food], ignore_index=True)
            st.session_state.df_food = new_df
            save_data_to_database_food()
            st.success("Lebensmittel erfolgreich hinzugefügt!")
            st.write(new_df)
        else:
            st.error("Bitte füllen Sie alle Felder aus.")

    if not st.session_state.df_food.empty:
        st.subheader("Aktuelle Lebensmittel im Kühlschrank")
        st.dataframe(st.session_state.df_food)
    else:
        st.write("Der Kühlschrank ist leer.")



def save_data_to_database_food():
    if 'github' in st.session_state:
        st.session_state.github.write_df(DATA_FILE_FOOD, st.session_state.df_food, "Updated food data")


def show_my_friends():
    st.write("Meine Freunde")

def show_settings():
    st.write("Einstellungen")



def save_data_to_database_food():
    if 'github' in st.session_state:
        st.session_state.github.write_df(DATA_FILE_FOOD, st.session_state.df_food, "Updated food data")

if __name__ == "__main__":
    main()
