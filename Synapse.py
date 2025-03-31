# Synapse.py
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

# # Welcome message (optional, only if no page is loaded)
# st.title("Welcome to SYNAPSE!") 


# # st.write("Navigate using the sidebar or page links.")

# col1, col2 = st.columns([5, 1])  # 4:1 ratio to push button to the right
# with col1:
#     st.write("👈 Navigate using the sidebar or page links 👉")
# with col2:
#     page_link = st.page_link("pages/1_Home.py",icon = "🏠")

# st.image("landing_page.jpg")



# Remove top white space
st.markdown("""
    <style>
    .main > div:first-child {
        padding-top: 0rem !important;
        margin-top: 0rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Helper to encode images
def get_image_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except FileNotFoundError:
        st.error(f"Error: Image file '{path}' not found in the project directory.")
        return None
    except Exception as e:
        st.error(f"Error converting image '{path}' to Base64: {str(e)}")
        return None

# Load images
human_base64 = get_image_base64("human.png")
robot_base64 = get_image_base64("robot.png")

# Style and layout
st.markdown(f"""
    <style>
    .welcome-text {{
        font-size: 4rem;
        font-weight: bold;
        text-align: center;
        color: {'black' if st.session_state.theme == 'Light' else 'white'};
        text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
        margin-top: 0;
        padding-top: 5px;
    }}
    .nav-hint {{
        text-align: center;
        font-size: 18px;
        color: {'black' if st.session_state.theme == 'Light' else 'white'};
        margin-top: 10px;
        margin-bottom: 0px;
    }}
    @keyframes slideInLeft {{
        from {{ transform: translateX(-100%); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
    @keyframes slideInRight {{
        from {{ transform: translateX(100%); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
    .image-row {{
        display: flex;
        justify-content: center;
        gap: 0px;
        flex-wrap: wrap;
        padding: 0 10px;
    }}
    .human {{
        width: 50%;
        max-width: 700px;
        height: auto;
        animation: slideInLeft 1.5s ease;
    }}
    .robot {{
        width: 50%;
        max-width: 700px;
        height: auto;
        animation: slideInRight 1.5s ease;
    }}
    </style>

    <div class="welcome-text">Welcome to SYNAPSE!</div>
    <div class="nav-hint">👈 Navigate using the sidebar or page links 👉</div>
""", unsafe_allow_html=True)

# Right-aligned Home/Login links
col1, col2, col3 = st.columns([6, 0.75, 1])
with col2:
    st.page_link("pages/1_Home.py", icon="🏠", label="Home")
with col3:
    st.page_link("pages/2_Login.py", icon="🔑", label="Login/Signup")

# Image section with animations
st.markdown(f"""
    <div class="image-row">
        <img src="data:image/png;base64,{human_base64}" class="human" alt="Human with medical report">
        <img src="data:image/png;base64,{robot_base64}" class="robot" alt="Robot">
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown(f"""
    <style>
    .footer {{
        text-align: center;
        padding: 10px;
        font-size: 14px;
        color: {'black' if st.session_state.theme == 'Light' else 'white'};
    }}
    </style>
    <div class="footer">
        © 2025 SYNAPSE. All rights reserved.
    </div>
""", unsafe_allow_html=True)
