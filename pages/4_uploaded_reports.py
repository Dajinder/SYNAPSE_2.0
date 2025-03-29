# pages/4_Uploaded_Reports.py
import streamlit as st
import pandas as pd
from utils import apply_theme, get_user_reports

# Set page config
st.set_page_config(page_title="Uploaded Reports", page_icon="📋")

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

def format_size(bytes_size):
    """Convert bytes to a human-readable format."""
    kb_size = bytes_size / 1024
    if kb_size < 1024:
        return f"{kb_size:.2f} KB"
    mb_size = kb_size / 1024
    return f"{mb_size:.2f} MB"

def main():
    st.sidebar.write(f"Logged in: {st.session_state.logged_in}")
    st.sidebar.write(f"Username: {st.session_state.username}")

    if not st.session_state.logged_in:
        st.warning("Please login first.")
        st.stop()
    else:
        st.title("Uploaded Reports Sorted by Date")
        st.write(f"Welcome, {st.session_state.username}!")

        # if st.session_state.reports:
        #     sorted_reports = sorted(st.session_state.reports, key=lambda x: x["upload_time"], reverse=True)

        # Retrieve reports from the database
        reports = get_user_reports(st.session_state.username)

        if reports:
            sorted_reports = sorted(reports, key=lambda x: x["upload_time"], reverse=True)
            col1, col2, col3, col4 = st.columns([2, 3, 2, 1])  # Adjust column widths
            with col1:
                st.write("**File Name**")
            with col2:
                st.write("**Upload Date**")
            with col3:
                st.write("**File Size**")
            with col4:
                st.write("**Download**")

            # Display table rows with download buttons
            for index, report in enumerate(sorted_reports):
                col1, col2, col3, col4 = st.columns([2, 3, 2, 1])
                with col1:
                    st.write(report["name"])
                with col2:
                    st.write(report["upload_time"].strftime("%Y-%m-%d %H:%M:%S"))
                with col3:
                    # Display file size if available, otherwise show 'N/A'
                    file_size = report.get("size", "N/A")
                    if file_size != "N/A":
                        st.write(format_size(file_size))
                    else:
                        st.write("N/A")
                with col4:
                    file_bytes = report["file"].getvalue()
                    st.download_button(
                        label="📥",
                        data=file_bytes,
                        file_name=report["name"],
                        mime=report["type"],
                        key=f"download_{index}"
                    )
        else:
            st.write("No reports uploaded yet.")

if __name__ == "__main__":
    main()