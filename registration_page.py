import streamlit as st
import datetime as dt
import pandas as pd
from src.helpers import connect_to_collection


def registration_page():
    placeholder = st.empty()

    with placeholder.form("Registration"):
        username = st.text_input("User Name*")
        email = st.text_input("E-Mail*")
        birth_date = st.date_input("Birth Date", value=None)
        password = st.text_input("Password*", type="password")
        repeat_password = st.text_input("Repeat Password*", type="password")
        submit_button = st.form_submit_button("Register")

    if submit_button:
        # define the database
        db_name = 'test_app'
        # define the collection
        collection_name = 'data'
        collection = connect_to_collection(db_name, collection_name)

        # read the data from the collection and identify usernames
        user_data = pd.DataFrame(list(collection.find()))
        usernames = list(user_data.username)

        if username in usernames:
            st.error("Username taken", icon="⚠️")
        elif len(username) < 1 and len(password) < 1:
            st.error("Please enter user name and password", icon="⚠️")
        elif len(username) < 1:
            st.error("Please enter a user name", icon="⚠️")
        elif len(password) < 1:
            st.error("Please enter a password", icon="⚠️")
        elif len(email) < 1:
            st.error("Please enter your email address", icon="⚠️")
        elif repeat_password != password:
            st.error("Passwords do not match", icon="⚠️")
        else:
            document = {
                "username": username,
                "email": email,
                "birth_date": f"{birth_date}",
                "password": password,
                "created_at": dt.datetime.now()
            }
            collection.insert_one(document)
            placeholder.empty()
            st.title("Ya done did it son")

