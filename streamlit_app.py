import streamlit as st
from firebase_config import auth_pyrebase, auth
import time

# Inject Custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Streamlit App Configuration
st.set_page_config(page_title="Spotflix", layout="centered")

# Session State Management
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

def login(email, password):
    try:
        user = auth_pyrebase.sign_in_with_email_and_password(email, password)
        if not user['emailVerified']:
            st.warning("Please verify your email before logging in.")
            return
        st.session_state.logged_in = True
        st.session_state.user = user
        st.success("Login successful!")
    except Exception as e:
        st.error(f"Login failed: {e}")

def logout():
    st.session_state.logged_in = False
    st.session_state.user = None

def sign_up(email, password):
    try:
        user = auth_pyrebase.create_user_with_email_and_password(email, password)
        auth_pyrebase.send_email_verification(user['idToken'])
        st.success("Sign-up successful! Please verify your email.")
    except Exception as e:
        st.error(f"Signup failed: {e}")

def send_password_reset(email):
    try:
        auth_pyrebase.send_password_reset_email(email)
        st.success("Password reset email sent. Check your inbox.")
    except Exception as e:
        st.error(f"Failed to send reset email: {e}")

def display_trailers():
    st.header("Available Trailers")
    st.video("https://www.youtube.com/watch?v=abc")

def display_subscription_content():
    st.header("Full Episodes")
    st.video("https://www.youtube.com/watch?v=xyz")

# UI Logic
st.title("🎬 Welcome to Spotflix")

if not st.session_state.logged_in:
    st.subheader("Log in to access content")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Login"):
            login(email, password)
    with col2:
        if st.button("Google Sign-In"):
            st.info("For now, use Email and Password.")
    with col3:
        if st.button("Forgot Password?"):
            send_password_reset(email)

    st.write("Don't have an account?")
    if st.button("Sign Up"):
        sign_up(email, password)

else:
    st.sidebar.button("Logout", on_click=logout, key="logout", 
                      use_container_width=True, css_class="sidebar-button")

    # Display Content
    if st.sidebar.button("View Trailers", key="trailers", 
                         use_container_width=True, css_class="sidebar-button"):
        display_trailers()

    if st.sidebar.button("View Full Episodes (Subscription Required)", key="episodes", 
                         use_container_width=True, css_class="sidebar-button"):
        display_subscription_content()
