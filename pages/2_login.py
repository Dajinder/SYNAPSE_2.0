# pages/2_Login.py
import streamlit as st
from utils import validate_user, register_user, apply_theme


# Set page config
st.set_page_config(page_title="Login", page_icon="🔑")

apply_theme()


# Top right theme toggle
col1, col2 = st.columns([7, 1])
with col2:
    dark_mode = st.toggle(
        "Light Mode" if st.session_state.theme == "Dark" else "Dark Mode",
        value=(st.session_state.theme == "Dark")
    )
    new_theme = "Dark" if dark_mode else "Light"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

st.logo(image="logo_6.png", size="large")

# Initialize session state if not already set
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if validate_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login Successful")
            st.rerun()  # Force rerun to update state across pages
        else:
            st.error("Invalid username or password")

def signup_page():
    st.title("Signup")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Signup"):
        if password == confirm_password:
            if register_user(username, password):
                st.success("Signup Successful! Please log in.")
            else:
                st.error("Username already exists.")
        else:
            st.error("Passwords do not match!")

def main():
    st.sidebar.write(f"Logged in: {st.session_state.logged_in}")  # Debug output
    st.sidebar.write(f"Username: {st.session_state.username}")
    if st.session_state.logged_in:
        st.title(f"Welcome, {st.session_state.username}! Please select a task from the sidebar.")

        col1, col2 = st.columns([2, 1])  # 4:1 ratio to push button to the right
        with col1:
            st.page_link("pages/3_upload_report.py", label="Upload Report", icon="📤")
            
        with col2:
            st.page_link("pages/4_uploaded_reports.py", label="Uploaded Reports", icon="📋")  # Links to Login page


        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
    else:
        task_mode = st.radio("Choose", ["Login", "Signup"])
        if task_mode == "Login":
            login_page()
        else:
            signup_page()

if __name__ == "__main__":
    main()