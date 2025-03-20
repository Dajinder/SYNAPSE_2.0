# pages/5_Subscription.py
import streamlit as st
from utils import apply_theme

# Set page config
st.set_page_config(page_title="Subscription", page_icon="💳")

apply_theme()


# Top right theme toggle
col1, col2 = st.columns([4, 1])
with col2:
    dark_mode = st.toggle("Dark Mode", value=(st.session_state.theme == "Dark"))
    new_theme = "Dark" if dark_mode else "Light"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

st.logo(image="logo_6.png", size="large")

def main():
    st.sidebar.write(f"Logged in: {st.session_state.logged_in}")
    st.sidebar.write(f"Username: {st.session_state.username}")

    if not st.session_state.logged_in:
        st.warning("Please login first.")
        st.stop()
    else:
        st.title("Subscription Plans")
        st.write(f"Welcome, {st.session_state.username}! Upgrade your account to unlock unlimited uploads.")

        # Subscription details
        st.subheader("Free Tier")
        st.write("- Upload up to 5 medical reports")
        st.write("- Basic report organization")
        st.write("- Free forever")

        st.subheader("Premium Plan - $9.99/month")
        st.write("- Unlimited medical report uploads")
        st.write("- Advanced report organization")
        st.write("- Priority support")
        st.write("- Access to future premium features")

        # Mock subscribe button
        if not st.session_state.subscribed:
            if st.button("Subscribe to Premium"):
                # Simulate subscription (replace with actual payment logic in production)
                st.session_state.subscribed = True
                st.success("Subscription successful! You now have unlimited uploads.")
                st.rerun()
        else:
            st.success("You are already subscribed to the Premium Plan!")
            st.write("Enjoy unlimited uploads and premium features.")

        # Back to upload page
        st.page_link("pages/3_upload_report.py", label="Back to Upload Reports", icon="📤")

if __name__ == "__main__":
    main()