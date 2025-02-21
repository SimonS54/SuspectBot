import firebase_admin
from firebase_admin import credentials, firestore

# Firebase setup
if not firebase_admin._apps:
    cred = credentials.Certificate("data/suspectbotdb.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
