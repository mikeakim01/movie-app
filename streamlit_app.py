import streamlit as st
from pymongo import MongoClient
import bcrypt

# MongoDB setup (replace <password> and <dbname> with your credentials)
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

# Login / Registration Screen
def login_page():
    st.title("Bongoflix Login")
    choice = st.sidebar.selectbox("Login or Register", ["Login", "Register"])
    
    if choice == "Login":
        st.subheader("Login to Bongoflix")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
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
        
        if st.button("Register"):
            if password != confirm_password:
                st.warning("Passwords do not match!")
            else:
                if register_user(username, password, email, phone):
                    st.success("Registration successful! Please login.")

# Main App Content (Only for Logged-in Users)
def main_app():
    st.title("Welcome to Bongoflix")
    
    # Sidebar for username and logout button
    with st.sidebar:
        if "username" in st.session_state:
            st.markdown(f"<h5 style='text-align: left;'>Logged in as: {st.session_state.username}</h5>", unsafe_allow_html=True)
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.success("Logged out successfully")
    
    st.write("Enjoy the best movie streaming experience.")

    # Fetch and display movies from MongoDB
    st.subheader("Featured Movies")
    
    # Fetch all movies from the collection
    try:
        movies = list(movies_collection.find())  # Convert the cursor to a list
        
        # Check if movies are present
        if not movies:
            st.write("No movies found in the database.")
        else:
            # Display each movie
            for movie in movies:
                st.write(f"**Title:** {movie['title']}")
                st.image(movie['thumbnailUrl'], width=150)  # Display movie thumbnail
                st.write(f"**Genre:** {movie['genre']}")
                st.write(f"**Duration:** {movie['duration']}")
               
                
    except Exception as e:
        st.error(f"Error fetching movies: {e}")

# Run the App Logic
if __name__ == "__main__":
    if st.session_state.logged_in:
        main_app()
    else:
        login_page()
