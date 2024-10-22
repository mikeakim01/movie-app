import streamlit as st
from pymongo import MongoClient
import bcrypt

# MongoDB connection setup
client = MongoClient("mongodb+srv://mike:Bil5tDBBKWVZ4cvs@cluster0.ylyymur.mongodb.net/cluster0")
db = client.cluster0  # Database
users_collection = db.users  # Users collection
movies_collection = db.Movie  # Movies collection

# Inject Custom CSS for Responsive Design
st.markdown(
    """
    <style>
    /* General layout adjustments */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    /* Increase font sizes for headers and buttons */
    h1, h2, h3, h4 {
        font-size: 1.5rem;
    }
    button {
        font-size: 1.2rem;
    }
    .stTextInput > div > input {
        font-size: 1.1rem;
    }
    .stButton > button {
        padding: 10px 20px;
        border-radius: 5px;
    }

    /* Improve responsiveness for smaller screens */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        h1, h2, h3 {
            font-size: 1.2rem;
        }
        button {
            font-size: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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

    # Display buttons side-by-side
    col1, col2 = st.columns(2)

    with col1:
        login_button = st.button("Login", key="login_button")
    with col2:
        register_button = st.button("Register", key="register_button")

    if login_button:
        st.subheader("Login to Bongoflix")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login", key="confirm_login"):
            if authenticate_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome {username}!")
            else:
                st.error("Invalid username or password")

    elif register_button:
        st.subheader("Register for Bongoflix")
        username = st.text_input("Choose a Username")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        password = st.text_input("Choose a Password", type="password")
        confirm_password = st.text_input("Re-enter Password", type="password")

        if st.button("Register", key="confirm_register"):
            if password != confirm_password:
                st.warning("Passwords do not match!")
            else:
                if register_user(username, password, email, phone):
                    st.success("Registration successful! Please login.")

# Main App Content (Only for Logged-in Users)
def main_app():
    st.title("Welcome to Bongoflix")

    # Top navigation bar for username and logout button
    st.write(f"Logged in as: **{st.session_state.username}**")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.success("Logged out successfully")

    st.subheader("Featured Movies")

    # Fetch all movies from the collection
    try:
        movies = list(movies_collection.find())  # Convert the cursor to a list

        if not movies:
            st.write("No movies found in the database.")
        else:
            cols = st.columns(3)  # Create columns for movie tiles

            for i, movie in enumerate(movies):
                with cols[i % 3]:
                    if st.button(f"{movie['title']}", key=movie['_id']):
                        st.session_state.selected_movie = movie
                        st.experimental_set_query_params(selected_movie=movie['_id'])

                    st.image(movie['thumbnailUrl'], width=150)
                    st.write(f"**Title:** {movie['title']}")

    except Exception as e:
        st.error(f"Error fetching movies: {e}")

    # Display selected movie details
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

# Run the App Logic
if __name__ == "__main__":
    if st.session_state.logged_in:
        main_app()
    else:
        login_page()
