from pymongo.mongo_client import MongoClient
import streamlit as st


@st.cache_resource
def connect_to_mongo():
    # load the user and db password from the secrets.toml file
    user = st.secrets['username']
    db_password = st.secrets['password']

    # This is our database connection string, for a cluster called tb-ii
    uri = f"mongodb+srv://{user}:{db_password}@ani-cluster.mvp6j.mongodb.net/?retryWrites=true&w=majority&appName=ani-Cluster"

    # Let's connect to our MongoClient
    client = MongoClient(uri)

    try:
        # print a message to say the
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")

        return client
    except Exception as e:
        # if connection was not made, then you will see an error message in your terminal
        print(e)


def connect_to_collection(db_name, collection_name):
    # connect to cluster
    client = connect_to_mongo()

    # connect to the collection
    db = client[db_name]
    collection = db[collection_name]

    return collection
