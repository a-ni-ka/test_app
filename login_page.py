import streamlit as st
import pandas as pd
from registration_page import registration_page
from src.helpers import connect_to_collection

st.set_page_config(page_title="Test App",
                   page_icon="🪄")

# setup counter, so we only see login page once
if 'count' not in st.session_state:
    st.session_state.count = 0

# also set up a credential check
if 'credentials_check' not in st.session_state:
    st.session_state.credentials_check = False


# create a placeholder variable, so I can delete the form widget after using it
placeholder = st.empty()


def login_page():
    with placeholder.form("Login"):
        st.write("Please enter your login data. If you haven't registered yet, please click 'Register'.")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")
        register_button = st.form_submit_button("Register")

    if login_button:
        db_name = "test_app"
        collection_name = "data"
        collection = connect_to_collection(db_name, collection_name)

        # check username
        # read the data from the collection and identify usernames
        user_data = pd.DataFrame(list(collection.find()))
        user_names = list(user_data.username)

        # check password
        if username in user_names:
            # this selects the password of the user that is entering information
            registered_password = list(user_data[user_data.username == username].password)[0]

            if password == registered_password:
                st.session_state.credentials_check = True
            else:
                st.error("The username/password is not correct")
        else:
            st.error("Please provide correct user name or click on register as new user")

    if register_button:
        st.session_state.count = 1
        placeholder.empty()


if st.session_state.count == 0:
    login_page()

if st.session_state.count == 1:
    registration_page()

if st.session_state.credentials_check:
    placeholder.empty()
    st.title("Welcome back!")
