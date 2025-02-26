import firebase_admin
from firebase_admin import credentials, firestore

# Firebase setup
# Initialize Firebase Admin SDK only if it hasn’t been initialized yet to avoid duplicate app errors
if not firebase_admin._apps:
    # Load the service account credentials from a JSON file
    cred = credentials.Certificate("data/suspectbotdb.json")  # Path to the Firebase service account key file
    # Initialize the Firebase app with the provided credentials
    firebase_admin.initialize_app(cred)

# Create a Firestore client instance for database interactions
db = firestore.client()  # Firestore database client used across the bot for data storage and retrieval