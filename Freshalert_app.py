import streamlit as st
import pandas as pd
from datetime import datetime, date

st.set_page_config(page_title="Fresh----Alert", page_icon="🗄️", layout="wide")

def init_dataframe():
    """Initialize or load the dataframe."""
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=['Name', 'Birth Date', 'Age'])
def calculate_ablauf(ablauf_date):
    """Calculate Ablaufdatum given the Ablauf date."""
    today = date.today()
    ablauf = today.year - ablauf_date.year - ((today.month, today.day) < (ablauf_date.month, ablauf_date.day))
    return ablauf


def add_entry(lebensmittel, ablauf_date):
    """Add a new entry to the DataFrame using pd.concat and calculate age."""
    age = calculate_ablauf(ablauf_date)
    new_entry = pd.DataFrame([{'lebensmittel': name, 'Ablaufdatum': ablauf_date, 'Ablauf': ablauf}])
    st.session_state.df = pd.concat([st.session_state.df, new_entry], ignore_index=True)

def display_dataframe():
    """Display the DataFrame in the app."""
    if not st.session_state.df.empty:
        st.dataframe(st.session_state.df)
    else:
        st.write("No data to display.")

def main():
    st.title("FreshAlert")

    init_dataframe()

    with st.sidebar:
        st.header("Add New Entry")
        name = st.text_input("Lebensmittel")
        ablauf_date = st.date_input("Ablaufdatum",min_value=date(1950, 1, 1),format="DD.MM.YYYY")
        add_button = st.button("Add")

    if add_button and name:  # Check if name is not empty
        add_entry(lebensmittel, ablauf_date)

    display_dataframe()
    plot_data()

if __name__ == "__main__":
    main()
