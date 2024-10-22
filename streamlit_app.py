import streamlit as st
from pymongo import MongoClient
import bcrypt

# Inline CSS to change background to maroon and text to white
page_bg_css = """
<style>
    body {
        background-color: maroon;
        color: white;
    }
    .stButton>button {
        background-color: white;
        color: maroon;
    }
</style>
"""
st.markdown(page_bg_css, unsafe_allow_html=True)

client = MongoClient("mongodb+srv://mike:Bil5tDBBKWVZ4cvs@cluster0.ylyymur.mongodb.net/cluster0")
db = client.cluster0  # Database
users_collection = db.users  # Users collection
movies_collection = db.Movie  # Movies collection

# User Authentication Functions
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

def authenticate_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and check_password(user["password"], password):
        return True
    return False

def register_user(username, password, email, phone):
    if users_collection.find_one({"username": username}):
        st.warning("Username already taken!")
        return False
    hashed_pw = hash_password(password)
    users_collection.insert_one({"username": username, "password": hashed_pw, "email": email, "phone": phone})
    st.success("User registered successfully!")
    return True

# Secure Login State Management
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.title("Bongoflix Login")
    choice = st.sidebar.selectbox("Login or Register", ["Login", "Register"])
    
    if choice == "Login":
        st.subheader("Login to Bongoflix")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", key="login_button"):
            if authenticate_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome {username}!")
            else:
                st.error("Invalid username or password")

    elif choice == "Register":
        st.subheader("Register for Bongoflix")
        username = st.text_input("Choose a Username")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        password = st.text_input("Choose a Password", type="password")
        confirm_password = st.text_input("Re-enter Password", type="password")
        
        if st.button("Register", key="register_button"):
            if password != confirm_password:
                st.warning("Passwords do not match!")
            else:
                if register_user(username, password, email, phone):
                    st.success("Registration successful! Please login.")

def main_app():
    st.title("Welcome to Bongoflix")

    with st.sidebar:
        if "username" in st.session_state:
            st.markdown(f"<h5 style='text-align: left;'>Logged in as: {st.session_state.username}</h5>", unsafe_allow_html=True)
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.success("Logged out successfully")

    st.write("Enjoy the best movie streaming experience.")
    st.subheader("Featured Movies")

    try:
        movies = list(movies_collection.find())

        if not movies:
            st.write("No movies found in the database.")
        else:
            cols = st.columns(3)
            for i, movie in enumerate(movies):
                with cols[i % 3]:
                    if st.button(f"{movie['title']}", key=movie['_id']):
                        st.session_state.selected_movie = movie
                        st.experimental_set_query_params(selected_movie=movie['_id'])
                        st.session_state.selected_movie = movie

                    st.image(movie['thumbnailUrl'], width=150)
                    st.write(f"**Title:** {movie['title']}")

    except Exception as e:
        st.error(f"Error fetching movies: {e}")

    if 'selected_movie' in st.session_state:
        selected_movie = st.session_state.selected_movie
        st.subheader("Selected Movie")
        st.image(selected_movie['thumbnailUrl'], width=200)
        st.write(f"**Title:** {selected_movie['title']}")
        st.write(f"**Description:** {selected_movie['description']}")
        st.write(f"**Genre:** {selected_movie['genre']}")
        st.write(f"**Duration:** {selected_movie['duration']}")

        video_html = f"""
        <video width="600" controls controlsList="nodownload">
            <source src="{selected_movie['videoUrl']}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
        """
        st.components.v1.html(video_html, height=400)

        if st.button("Back to Movie List"):
            del st.session_state.selected_movie
            st.experimental_set_query_params()

if __name__ == "__main__":
    if st.session_state.logged_in:
        main_app()
    else:
        login_page()
