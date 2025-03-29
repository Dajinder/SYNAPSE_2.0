# SYNAPSE - Diagnostic Report Management App

## Overview
SYNAPSE is a multi-page Streamlit application designed to allow users to upload, view, and manage diagnostic reports (PDFs or images). The app includes features like user authentication, subscription management, and report preview with text extraction. Users can sign up, log in, upload reports, view uploaded reports, and subscribe for unlimited uploads.

## Features
- User authentication (signup and login) with email and password validation.
- Upload diagnostic reports (PDF or image formats).
- Preview uploaded reports and extract text using OCR (for images) and PDF text extraction.
- View a list of uploaded reports sorted by date.
- Subscription system to allow unlimited report uploads.
- Light/Dark theme toggle in the sidebar.
- Persistent sidebar with logo and app name across all pages.

## Tech Stack
- **Frontend/Backend**: Streamlit (Python)
- **Database**: SQLite (`users.db` for user data, `reports.db` for report data)
- **Libraries**:
  - `PyPDF2`: PDF text extraction
  - `pdfplumber`: Fallback PDF text extraction
  - `pdf2image`: PDF-to-image conversion for previews
  - `pytesseract`: OCR for image text extraction
  - `Pillow`: Image processing
- **Deployment**: Streamlit Community Cloud (linked to GitHub)

## File Structure
   synapse-app/
      |-- app.py                    # Main app file (landing page)
      |-- utils.py                  # Utility functions (database, text extraction, theme, etc.)
      |-- requirements.txt          # Python dependencies
      |-- packages.txt              # System dependencies for Streamlit Community Cloud
      |-- README.md                 # Project documentation
      |-- logo_3.jpg                # Logo image for sidebar
      |-- landing_page.jpg          # Landing page image
      |-- pages/                    # Directory for multi-page app
      |   |-- 1_home.py             # Home page
      |   |-- 2_login.py            # Login and signup page
      |   |-- 3_upload_report.py    # Report upload page
      |   |-- 4_uploaded_reports.py # View uploaded reports page
      |   |-- 5_subscription.py     # Subscription page
      |-- users.db                  # SQLite database for user data (created on first run)
      |-- reports.db                # SQLite database for report data (created on first run)


## Installation (Local Setup)
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/synapse-app.git
   cd synapse-app

2. Install Python dependencies:
   pip install -r requirements.txt

3. Install Poppler for PDF-to-image conversion
   Download Poppler binaries from a trusted source (e.g., Poppler for Windows).
   Add the bin/ directory to your system PATH.

4. Run the app locally:
   streamlit run Synapse.py

## Usage
1. *Home Page*: Start at the landing page (Synapse.py) and navigate to the Home page (1_Home.py).
2. *Signup/Login*: Go to the Login page (2_Login.py) to sign up or log in. Email and password validation is enforced during signup.
3. *Upload Reports*: After logging in, use the Upload Diagnostic Report page (3_Upload_Report.py) to upload PDFs or images. Free users are limited to 5 uploads.
4. *View Reports*: View your uploaded reports on the Uploaded Reports page (4_Uploaded_Reports.py), sorted by date.
5. *Subscribe*: Subscribe for unlimited uploads on the Subscription page (5_Subscription.py).
6. *Theme Toggle*: Use the sidebar to switch between Light and Dark themes.

## Contributing
Fork the repository.
Create a new branch for your feature:
Make changes, commit, and push:
   git add .
   git commit -m "Added feature"
   git push origin feature-name