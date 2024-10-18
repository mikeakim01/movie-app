import firebase_admin
from firebase_admin import credentials, auth
import pyrebase

# Load Firebase credentials
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)

# Pyrebase configuration
firebase_config = {
    "type": "service_account",
    "apiKey": "AIzaSyCWqIBXEyFk9nHJc5UyEaCvHmgVrjKrzCE",
    "authDomain": "pure-mission-337016.firebaseapp.com",
    "projectId": "pure-mission-337016",
    "storageBucket": "pure-mission-337016.appspot.com",
    "messagingSenderId": "976188288424",
    "appId": "1:976188288424:web:b64f0c6a1447958369c19d"
}

firebase = pyrebase.initialize_app(firebase_config)
auth_pyrebase = firebase.auth()
db = firebase.database()  # Optional if you use Firebase Realtime Database
