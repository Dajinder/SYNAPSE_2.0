# app.py
import streamlit as st
from utils import init_db, apply_theme, add_theme_toggle_to_sidebar
import base64

# Initialize the database
init_db()

# Session state initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'reports' not in st.session_state:
    st.session_state.reports = []
if 'subscribed' not in st.session_state:
    st.session_state.subscribed = False  # Default to free tier (not subscribed)

# Set page config for the main page
st.set_page_config(page_title="SYNAPSE", page_icon="🏠", layout="wide")

apply_theme()

# Add theme toggle to sidebar
add_theme_toggle_to_sidebar()

# # Top right theme toggle
# col1, col2 = st.columns([7.3, 1])
# with col2:
#     dark_mode = st.toggle("Dark Mode", value=(st.session_state.theme == "Dark"))
#     new_theme = "Dark" if dark_mode else "Light"
#     if new_theme != st.session_state.theme:
#         st.session_state.theme = new_theme
#         st.rerun()

# Sidebar navigation (Streamlit auto-generates this from page files)
st.logo(image="logo_6.png", size="large")
# st.sidebar.title("SYNAPSE")
# st.sidebar.write(f"Logged in: {st.session_state.logged_in}")
if st.session_state.logged_in and st.session_state.username:
    st.sidebar.write(f"Username: {st.session_state.username}")
    st.sidebar.write(f"Subscribed: {'Yes' if st.session_state.subscribed else 'No'}")  # Show subscription status

# Welcome message (optional, only if no page is loaded)
st.title("Welcome to SYNAPSE!") 


# st.write("Navigate using the sidebar or page links.")

col1, col2 = st.columns([5, 1])  # 4:1 ratio to push button to the right
with col1:
    st.write("👈 Navigate using the sidebar or page links 👉")
with col2:
    page_link = st.page_link("pages/1_Home.py",icon = "🏠")

st.image("landing_page.jpg")
