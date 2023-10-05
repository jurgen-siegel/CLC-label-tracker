
import streamlit as st
import user_auth
import main_content

# MongoDB setup and other initial configurations can be added here

if not st.session_state.get('logged_in'):
    # Display Registration and Login UI
    # This will use functions from user_auth.py
else:
    # Display main app content
    main_content.display_main_content()