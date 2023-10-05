import streamlit as st
import pandas as pd
from pymongo import MongoClient
import io
import matplotlib.pyplot as plt
import os
from werkzeug.security import generate_password_hash, check_password_hash

# Layout settings
st.set_page_config(layout="wide")

# Retrieve MongoDB URI from environment variable
MONGO_URI = os.environ.get("MONGO_URI")
if not MONGO_URI:
    st.error("Missing MongoDB URI. Please set the MONGO_URI environment variable.")
    st.stop()

# Connect to MongoDB using the retrieved URI
client = MongoClient(MONGO_URI)
db = client.label_tracker
collection = db.tickets

# Create a new collection for ticket history
ticket_history_collection = db.ticket_history

# Create a collection for users
users_collection = db.users


# Function to log ticket actions
def log_ticket_action(ticket_num, action, description=""):
    """ Log ticket actions to the ticket_history collection.
    Parameters:
    - ticket_num: The ticket number associated with the action.
    - action: The type of action (e.g., "added", "updated", "deleted").
    - description: A description or summary of the changes made. """
    history_entry = {
        'Ticket #': ticket_num,
        'Action': action,
        'Timestamp': pd.Timestamp.now(),
        'Description': description
    }
    ticket_history_collection.insert_one(history_entry)


# Function to handle sign-up
def handle_signup():
    st.subheader('Sign Up')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    confirm_password = st.text_input('Confirm Password', type='password')

    if st.button('Sign Up'):
        # Check if username already exists
        existing_user = users_collection.find_one({'username': username})
        if existing_user:
            st.warning('Username already exists. Please choose another.')
        elif password != confirm_password:
            st.warning('Passwords do not match. Please try again.')
        else:
            # Hash the password and store the user details in the database
            hashed_password = generate_password_hash(password, method='sha256')
            users_collection.insert_one({'username': username, 'password': hashed_password})
            st.success('Account created successfully! Please log in.')

    st.write('Already have an account? [Log in](#login)')


# Function to handle login
def handle_login():
    st.subheader('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        user = users_collection.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            st.session_state.logged_in_user = username
            st.success('Logged in successfully! Redirecting to main page...')
            st.write('If not redirected, [click here](#main).')
        else:
            st.warning('Incorrect username or password. Please try again.')

    st.write('Don\'t have an account? [Sign Up](#signup)')


# Function to handle logout
def handle_logout():
    if st.button('Logout'):
        del st.session_state.logged_in_user
        st.write('Logged out successfully! Redirecting to login page...')
        st.write('If not redirected, [click here](#login).')


# Main interface modifications for authentication
if 'logged_in_user' in st.session_state:
    st.write(f"Welcome, {st.session_state.logged_in_user}!")
    handle_logout()

    # Your ticket management code goes here
    st.subheader('Ticket Management Placeholder')
    st.write("You can add your ticket management functionality here.")
    st.write("This is a placeholder for managing tickets.")
    st.write("Add, edit, and delete tickets as needed.")

else:
    action = st.radio("Choose an action:", ["Login", "Sign Up"])
    if action == "Login":
        handle_login()
    elif action == "Sign Up":
        handle_signup()

st.write("--------------------------------------------------------------------------")
st.markdown("**Note: To manage tickets, follow these steps:**")
st.write("1. Write down the ticket number, name, and description.")
st.write("2. Check the appropriate boxes to indicate progress.")
st.write("3. Click 'Add Ticket' to create a new ticket.")

st.write("To edit an existing ticket:")
st.write("1. Pick the ticket number you want to modify.")
st.write("2. Make the necessary changes.")
st.write("3. Click 'Update Ticket' to save your changes.")

st.write("To view all tickets, click on 'Display Tickets' at the top of the page.")
