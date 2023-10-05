
import streamlit as st
from pymongo import MongoClient
import hashlib

def simple_hash(s):
    return str(hash(s))

def register_user(collection, reg_username, reg_password, reg_email):
    user_exists = collection.find_one({"username": reg_username})
    if user_exists:
        return "Username already exists. Please choose another."
    else:
        hashed_password = simple_hash(reg_password)
        user_data = {
            "username": reg_username,
            "password": hashed_password,
            "email": reg_email
        }
        collection.insert_one(user_data)
        return "Registration successful. Please log in."

def login_user(collection, login_username, login_password):
    user_details = collection.find_one({"username": login_username})
    if user_details:
        if user_details["password"] == simple_hash(login_password):
            return True, f"Welcome, {login_username}!"
        else:
            return False, "Incorrect password. Please try again."
    else:
        return False, "Username not found. Please register or try another username."