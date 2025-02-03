import streamlit as st
import pandas as pd
import datetime
import firebase_admin
from firebase_admin import credentials, firestore

"""
    credentials obtained through the streamlit community
    st secrets toml file. The toml file must have a [firebase]
    section formatted as follows:
    
    [firebase]
    type = "service_account"
    project_id = "XXX"
    private_key_id = "XXX"
    private_key = "XXX"
    client_email = "XXX"
    client_id = "XXX"
    auth_uri = "https://accounts.google.com/o/oauth2/auth"
    token_uri = "https://oauth2.googleapis.com/token"
    auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
    client_x509_cert_url = "XXX"
    
    The values may be obtained through creating a json credentials file
    from the firestore console.
"""

class FirestoreClient:
    def __init__(self):
        self.db = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate to Firestore only if not already authenticated."""
        if "db" not in st.session_state:
            # Initialize Firebase Admin SDK
            cred = credentials.Certificate(dict(st.secrets["firebase"]))
            firebase_admin.initialize_app(cred)
            
            # Initialize Firestore client
            st.session_state.db = firestore.client(database_id="ao-health-data")

        self.db = st.session_state.db

    def save_objective_snapshot(systolic,diastolic,heart_rate,glucose):
        user_id = "user_123"  # Replace with dynamic user auth if needed
        timestamp = datetime.datetime.utcnow().isoformat()
        data = {
            "systolic": systolic,
            "diastolic": diastolic,
            "heart_rate": heart_rate,
            "glucose": glucose,
            "timestamp": timestamp
        }
    
        # Save data to Firestore
        self.db.collection("users").document(user_id).collection("objectives").document(timestamp).set(data)

    def get_all_objective_snapshots():
        objective_snapshot_ref = self.db.collection("users").document("user_123").collection("objectives")

        # buggy code that tries to limit objectives to a timestamp range (doesn't work yet)
        # query = objective_snapshot_ref.where("timestamp", ">=", start_date_stamp).where("timestamp", "<=", end_date_stamp)
    
        query = objective_snapshot_ref.get()
        
        # Process results
        data = []
        for doc in query:
            doc_data = doc.to_dict()
            data.append({
                "Systolic": doc_data.get("systolic"),
                "Diastolic": doc_data.get("diastolic"),
                "HeartRate": doc_data.get("heart_rate"),
                "Glucose": doc_data.get("glucose"),
                "Timestamp": doc_data.get("timestamp")
            })

        if data:
            df = pd.DataFrame(data)
            return df
        else return None
  
    """
    def get_collection(self, collection_path: str):
        """Returns a reference to a Firestore collection."""
        return self.db.collection(collection_path)

    def get_document(self, collection_path: str, document_id: str):
        """Returns a reference to a specific document."""
        return self.db.collection(collection_path).document(document_id)

    def query_collection(self, collection_path: str, field: str, operator: str, value):
        """Query a collection based on specific conditions."""
        collection_ref = self.db.collection(collection_path)
        query = collection_ref.where(field, operator, value)
        return query.get()

    def get_all_documents(self, collection_path: str):
        """Get all documents from a collection."""
        collection_ref = self.db.collection(collection_path)
        return collection_ref.get()
    """
