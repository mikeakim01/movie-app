import firebase_admin
from firebase_admin import credentials, auth
import pyrebase

# Load Firebase credentials
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)

# Pyrebase configuration
firebase_config = {
    "apiKey": "a",
    "authDomain": "b",
    "projectId": "c",
    "storageBucket": "d",
    "messagingSenderId": "e",
    "appId": "f"
}

firebase = pyrebase.initialize_app(firebase_config)
auth_pyrebase = firebase.auth()
db = firebase.database()  # Optional if you use Firebase Realtime Database
