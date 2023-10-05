
import streamlit as st
import user_auth
import main_content

# MongoDB setup and other initial configurations can be added here

if not st.session_state.get('logged_in'):
    # Display Registration and Login UI
    user_auth.display_login_registration_ui()
else:
    # Display main app content
    main_content.display_main_content()