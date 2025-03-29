# pages/3_Upload_Report.py
import streamlit as st
from utils import extract_text_from_pdf, extract_text_from_image, convert_pdf_to_images, apply_theme, get_user_reports, save_report, add_theme_toggle_to_sidebar
import io
import datetime
from PIL import Image

# Set page config
st.set_page_config(page_title="Upload Report", page_icon="📤")

apply_theme()

# Add theme toggle to sidebar
add_theme_toggle_to_sidebar()

# # Top right theme toggle
# col1, col2 = st.columns([4, 1])
# with col2:
#     dark_mode = st.toggle("Dark Mode", value=(st.session_state.theme == "Dark"))
#     new_theme = "Dark" if dark_mode else "Light"
#     if new_theme != st.session_state.theme:
#         st.session_state.theme = new_theme
#         st.rerun()

st.logo(image="logo_6.png", size="large")

def main():
    # Debug output in sidebar
    st.sidebar.write(f"Logged in: {st.session_state.logged_in}")
    st.sidebar.write(f"Username: {st.session_state.username}")

    if not st.session_state.logged_in:
        st.warning("Please login first.")
        st.stop()  # Stop execution if not logged in
    else:
        # st.title("Upload Diagnostic Report")

        col1, col2 = st.columns([5, 1])  # 4:1 ratio to push button to the right
        with col1:
            st.title("Upload Diagnostic Report")
            
        with col2:
            
            st.page_link("pages/4_Uploaded_Reports.py", label="Uploaded Reports", icon="📋")  # Links to Login page


        # st.write(f"Welcome, {st.session_state.username}!")  # Confirm user

        # Fetch the user's reports from the database to check the count
        user_reports = get_user_reports(st.session_state.username)
        report_count = len(st.session_state.reports)
        max_free_reports = 5

        if not st.session_state.subscribed and report_count >= max_free_reports:
            st.error(f"You have reached the limit of {max_free_reports} free uploads.")
            st.write("Please subscribe to upload more reports.")
            st.page_link("pages/5_Subscription.py", label="Go to Subscription", icon="💳")
            st.stop()
        
        else:

            uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])

            if uploaded_file:
                file_type = uploaded_file.type
                extracted_text = ""
                images = []

                if file_type == "application/pdf":
                    st.info("Processing PDF file...")
                    images = convert_pdf_to_images(uploaded_file)
                    uploaded_file.seek(0)
                    extracted_text = extract_text_from_pdf(uploaded_file)
                elif file_type.startswith("image/"):
                    st.info("Processing Image file...")
                    image = Image.open(uploaded_file)
                    extracted_text = extract_text_from_image(image)
                    images = [image]

                col1, col2 = st.columns(2)
                with col1:
                    st.header("Report Preview")
                    if images:
                        for img in images:
                            st.image(img, caption="Page Preview", use_container_width=True)
                    else:
                        st.warning("No preview available.")
                with col2:
                    st.header("Extracted Text")
                    if extracted_text:
                        st.text_area("  ", extracted_text, height=460)
                    else:
                        st.warning("No text extracted.")

                # upload_time = datetime.datetime.now()
                # file_bytes = io.BytesIO(uploaded_file.getvalue())
                # file_size = file_bytes.getbuffer().nbytes


                # Save the report to the database
                upload_time = datetime.datetime.now()
                file_bytes = uploaded_file.getvalue()  # Get raw bytes for database storage
                file_size = len(file_bytes)

                # Save to database
                save_report(
                    username=st.session_state.username,
                    file_name=uploaded_file.name,
                    file_data=file_bytes,  # Store as BLOB
                    upload_time=upload_time,
                    file_type=file_type,
                    file_size=file_size
                )

                # # Update session state for immediate display (optional, can be removed if fully relying on DB)
                # if 'reports' not in st.session_state:
                #     st.session_state.reports = []
                # st.session_state.reports.append({
                #     "name": uploaded_file.name,
                #     "file": io.BytesIO(file_bytes),
                #     "upload_time": upload_time,
                #     "type": file_type,
                #     "size": file_size
                # })

                # Show a success message
                st.success("Report uploaded successfully!")

                # Check the updated report count after upload
                user_reports = get_user_reports(st.session_state.username)
                report_count = len(user_reports)

                # Show warning when reaching the limit
                if not st.session_state.subscribed and len(st.session_state.reports) == max_free_reports:
                    st.warning(f"You have reached the maximum of {max_free_reports} free uploads! Subscribe to upload more.")
                    st.page_link("pages/5_Subscription.py", label="Subscribe Now", icon="💳")

if __name__ == "__main__":
    main()