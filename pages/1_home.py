# pages/1_Home.py
import streamlit as st
import base64
import os
import time
from utils import apply_theme

# Set page config (must be at the top)
st.set_page_config(page_title="Home", page_icon="🏠")

apply_theme()


# Top right theme toggle
col1, col2 = st.columns([7, 1])
with col2:
    dark_mode = st.toggle("Dark Mode", value=(st.session_state.theme == "Dark"))
    new_theme = "Dark" if dark_mode else "Light"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

st.logo(image="logo_6.png", size="large")

def get_base64_image(file_path):
    """Convert local image to base64."""
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def main():
    # Top row with title and login button
    col1, col2 = st.columns([10, 1])  # 4:1 ratio to push button to the right
    with col1:
        st.title("SYNAPSE")
    with col2:
        st.page_link("pages/2_Login.py", label="Login/Signup", icon="🔒")  # Links to Login page

    st.write("Facing challenges while organizing your Medical Report? 😖")
    st.write("No more keeping track of your individual report! Welcome to the one-stop solution.")
    st.markdown('''
        1. Organizing all your medical reports.
        2. Keeping track at your fingertips.
        3. Having access anywhere & anytime.
    ''')

    # Image container
    with st.container():
        st.subheader("Explore SYNAPSE Features")
        
        # Define image directory and specific image files
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_dir = os.path.join(script_dir, "static")
        image_names = ["img_1.png", "img_2.png", "img_3.png", "img_4.jpg", "img_5.jpg"]
        image_paths = [os.path.join(image_dir, name) for name in image_names]
        
        # Convert images to base64
        image_urls = []
        for img_path in image_paths:
            base64_img = get_base64_image(img_path)
            image_urls.append(f"data:image/png;base64,{base64_img}")

        # Create a placeholder for the image
        placeholder = st.empty()

        # Fixed-size container with centered images
        while True:
            for url in image_urls:
                placeholder.markdown(f"""
                <div style="width: 600px; height: 300px; margin: auto; overflow: hidden; display: flex; justify-content: center; align-items: center; border: 1px solid #ccc;">
                    <img src="{url}" style="max-width: 100%; max-height: 100%; object-fit: contain;">
                </div>
                """, unsafe_allow_html=True)
                time.sleep(3)  # Change image every 3 seconds

if __name__ == "__main__":
    main()