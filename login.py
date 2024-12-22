import streamlit as st
from supabase import create_client, Client
import bcrypt
import re
import os
import jwt
import datetime
# from dotenv import load_dotenv

# Load .env file for environment variables (uncomment this if using actual env variables)
# load_dotenv()

# # Configure Supabase
# SUPABASE_URL = 'https://mylvpdlslvkpuhepzjpw.supabase.co'  # Replace with your Supabase URL
# SUPABASE_KEY = 'YOUR_SUPABASE_KEY'  # Replace with your Supabase key

# supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# # JWT Secret - Add it to your environment or load it from .env
# JWT_SECRET = "your_jwt_secret"  # Replace with your actual secret

def set_page_config():
    """Set the initial page configuration."""
    st.set_page_config(
        page_icon="",
        page_title="Breast Cancer Analysis",
        layout="wide",
        initial_sidebar_state="expanded",
    )

def inject_custom_css():
    """Inject custom CSS for styling."""
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #FFFFFF;
        }
        /* Styling for the sidebar */
        [data-testid="stSidebar"] {
            background-color: #FFB3D9;
            color: white;
        }
        /* Center the form container */
        .form-container {
            max-width: 400px;
            margin: auto;
            padding: 40px;
            background-color: #FFFFFF;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            text-align: center;
        }

        /* Styling for the form title */
        .form-title {
            font-size: 2rem;
            color: #8A2C52;
            font-weight: bold;
            margin-bottom: 20px;
            font-family: 'Poppins', sans-serif;
        }

        /* Input field styling */
        .stTextInput > div > div > input {
            width: 100%;
            padding: 12px;
            padding-left: 10px;
            border-radius: 8px;
            font-size: 1rem;
            border: 1px solid #E0E0E0;
            background-color: #F7F9FC;
            color: #333333;
            margin-bottom: 20px;
        }

        /* Button styling */
        .stButton > button {
            background-color: #A65277;
            color: white;
            font-size: 1rem;
            font-weight: bold;
            padding: 12px 20px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            width: 100%;
        }

        /* Hover effect for button */
        .stButton > button:hover {
            background-color: #C2185B;
        }

        /* Link styling for additional actions */
        .footer-text {
            color: #333;
            font-size: 0.9rem;
            margin-top: 20px;
        }

        .footer-text a {
            color: #8A2C52;
            text-decoration: none;
            font-weight: bold;
        }

        .footer-text a:hover {
            text-decoration: underline;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_sidebar():
    """Render the sidebar with navigation."""
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align: center;">
                <img src='https://github.com/shaniawardani/Breast-Cancer-/blob/main/asset/logo.png?raw=true' class='sidebar-logo'/>
            </div>
            """, unsafe_allow_html=True
        )
        # Language selection in the sidebar
        language = st.selectbox('Choose your language / Pilih bahasa Anda', ['en', 'id'])
        st.session_state['language'] = language


def is_valid_email(email):
    """Validates email using regex."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)


def login_form():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # Email validation
    if email and not is_valid_email(email):
        st.error("Invalid email format. Please enter a valid email address.")

    if st.button("Login"):
        if login(email, password):
            st.session_state['logged_in'] = True  
            st.session_state['email'] = email 
            st.success("Login successful!")
            st.experimental_rerun()  # Refresh the app
        else:
            st.error("Invalid email or password, Sign Up first if unregistered")


def verify_password(password, hashed):
    """Verify password using bcrypt."""
    return bcrypt.checkpw(password.encode(), hashed.encode())


def login(email, password):
    """Authenticate the user with Supabase."""
    response = supabase.from_('user').select("*").eq("email", email).execute()
    if response.data:
        user = response.data[0]
        if verify_password(password, user['password']):
            st.session_state['username'] = user['username']
            return True
    return False


def logout():
    """Log out the user by clearing session state."""
    del st.session_state['logged_in']
    del st.session_state['username']
    del st.session_state['email']
    st.success("You have been logged out!")


def main():
    inject_custom_css()
    render_sidebar()

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        st.write(f"Welcome, {st.session_state['username']}!")

        # Add a logout button
        if st.button("Log Out"):
            logout()
            st.session_state['logged_in'] = False  # Set to False so it will show login form again
            st.experimental_rerun()  # Refresh the app to show login form again
    else:        
        login_form()


if __name__ == '__main__':
    main()
