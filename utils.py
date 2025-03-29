# utils.py
import sqlite3
import PyPDF2
from pdf2image import convert_from_bytes
import pdfplumber
import pytesseract
from PIL import Image
import io
import datetime
import streamlit as st

# SQLite DB Setup for users and reports
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    # Reports table
    c.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            file_name TEXT,
            file_data BLOB,
            upload_time TEXT,
            file_type TEXT,
            file_size INTEGER,
            FOREIGN KEY (username) REFERENCES users(username)
        )
    """)
    conn.commit()
    conn.close()

# Register a new user
def register_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Validate user login
def validate_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

# Save a report to the database
def save_report(username, file_name, file_data, upload_time, file_type, file_size):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO reports (username, file_name, file_data, upload_time, file_type, file_size)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (username, file_name, file_data, upload_time.isoformat(), file_type, file_size))
    conn.commit()
    conn.close()

# Retrieve reports for a user
def get_user_reports(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM reports WHERE username = ?", (username,))
    reports = c.fetchall()
    conn.close()
    # Convert database rows to the same format as st.session_state.reports
    formatted_reports = []
    for report in reports:
        formatted_reports.append({
            "report_id": report[0],
            "username": report[1],
            "name": report[2],
            "file": io.BytesIO(report[3]),  # Convert BLOB back to BytesIO
            "upload_time": datetime.datetime.fromisoformat(report[4]),
            "type": report[5],
            "size": report[6]
        })
    return formatted_reports

# Extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text() or ""
    except Exception as e:
        try:
            file.seek(0)
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            return None
    return text

# Extract text from image
def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

# Convert PDF to images
def convert_pdf_to_images(pdf_file):
    try:
        images = convert_from_bytes(pdf_file.read())
        return images
    except Exception as e:
        return []
    
# Apply theme function
def apply_theme():
    if 'theme' not in st.session_state:
        st.session_state.theme = "Light"  # Default to Light theme

        

    if st.session_state.theme == "Light":
        st.markdown("""
            <style>
            .stApp {
                background-color: #ffffff;  /* Light orange background */
                color: #31333f;  /* Dark gray text */
            }
            h1, h2, h3, h4, h5, h6 {
                color: #31333f;  /* Orange headers */
            }
            .stButton>button {
                background-color: #FF9800;  /* Orange buttons */
                color: white;
                border: none;
            }
            .stButton>button:hover {
                background-color: #F57C00;  /* Darker orange on hover */
            }
            .stSuccess {
                color: #4CAF50;  /* Green for success messages */
            }
            [data-testid="stSidebar"] {
                background-color: #FF9800;  /* Orange sidebar */
            }
            </style>
        """, unsafe_allow_html=True)
    elif st.session_state.theme == "Dark":
        st.markdown("""
            <style>
            .stApp {
                background-color: #0e1117;  /* Dark gray background */
                color: #fafafa;  /* White text */
            }
            h1, h2, h3, h4, h5, h6 {
                color: #ffffff;  /* Purple headers */
            }
            .stButton>button {
                background-color: #bb86fc;  /* Purple buttons */
                color: #ffffff;  /* Black text on buttons */
                border: none;
            }
            .stButton>button:hover {
                background-color: #9a67ea;  /* Darker purple on hover */
            }
            .stSuccess {
                color: #03dac6;  /* Teal for success messages */
            }
            [data-testid="stSidebar"] {
                background-color: #262730;  /* Darker gray sidebar */
                color: #fafafa;  /* Light gray text in sidebar for better contrast */
            }
            .e1tphpha6 {
                color: #ffffff;  /* Light gray color for page links in sidebar */
            }
            [data-testid="stSidebarNavLink"] a:hover {
                color: #FFFFFF;  /* White on hover for page links */
            }
            [data-testid="stMarkdownContainer"]{
                color:#FFFFFF;
            }

            </style>
        """, unsafe_allow_html=True)

# Add a function to create the theme toggle in the sidebar
def add_theme_toggle_to_sidebar():
    # st.sidebar.markdown("---")
    dark_mode = st.sidebar.toggle(
        "Dark Mode" if st.session_state.theme == "Light" else "Light Mode",
        value=(st.session_state.theme == "Dark"),
        key="theme_toggle"
    )
    new_theme = "Dark" if dark_mode else "Light"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()