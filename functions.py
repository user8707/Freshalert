# functions.py

import streamlit as st
import pandas as pd
from github_contents import GithubContents
from constants import DATA_FILE, DATA_COLUMNS, DATA_FILE_FOOD, DATA_COLUMNS_FOOD

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

def save_data_to_database_login():
    st.session_state.github.write_df(DATA_FILE, st.session_state.df_login, "Updated registration data")

def save_data_to_database_food():
    if 'github' in st.session_state:
        st.session_state.github.write_df(DATA_FILE_FOOD, st.session_state.df_food, "Updated food data")
