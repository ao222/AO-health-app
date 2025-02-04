import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
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
            if not firebase_admin._apps:  # Check if Firebase app has been initialized
                cred = credentials.Certificate(dict(st.secrets["firebase"]))
                firebase_admin.initialize_app(cred)
            
            # Initialize Firestore client
            st.session_state.db = firestore.client(database_id="ao-health-data")

        self.db = st.session_state.db

    def save_objective_snapshot(self,systolic,diastolic,heart_rate,glucose):
        user_id = "user_123"  # Replace with dynamic user auth if needed
        timestamp = datetime.utcnow().isoformat()
        data = {
            "systolic": systolic,
            "diastolic": diastolic,
            "heart_rate": heart_rate,
            "glucose": glucose,
            "timestamp": timestamp
        }
    
        # Save data to Firestore
        self.db.collection("users").document(user_id).collection("objectives").document(timestamp).set(data)

    def save_daily_snapshot(self, date, sleep_hours, naps, walking_minutes, lifting_minutes, calories):
        user_id = "user_123"
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        data = {
            "date": today,
            "sleep_hours": sleep_hours,
            "naps": naps,
            "walking_minutes": walking_minutes,
            "lifting_minutes": lifting_minutes,
            "calories": calories
        }

        # Save data to Firestore
        self.db.collection("users").document(user_id).collection("dailies").document(today).set(data)
        
    def get_all_objective_snapshots(self):
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
        else:
            return None
            
    def get_objective_snapshots(self,from_timestamp, to_timestamp):
        start_time_str = from_timestamp.isoformat()
        end_time_str = to_timestamp.isoformat()

        # Reference Firestore objectives collection
        objective_snapshot_ref = self.db.collection("users").document("user_123").collection("objectives")
        
        # Query Firestore using document IDs (which are ISO formatted timestamps)
        query = (
            objective_snapshot_ref
            .order_by("__name__")  # Query based on document ID
            .start_at([start_time_str])  # Start at documents created at or after start_time
            .end_at([end_time_str])  # End at documents created at or before end_time
        )
        
        # Execute query and fetch documents
        docs = query.stream()
        
        # Process results
        data = []
        for doc in docs:
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
        else:
            return None
    """
    def get_collection(self, collection_path: str):
        #Returns a reference to a Firestore collection.
        return self.db.collection(collection_path)

    def get_document(self, collection_path: str, document_id: str):
        #Returns a reference to a specific document.
        return self.db.collection(collection_path).document(document_id)

    def query_collection(self, collection_path: str, field: str, operator: str, value):
        #Query a collection based on specific conditions.
        collection_ref = self.db.collection(collection_path)
        query = collection_ref.where(field, operator, value)
        return query.get()

    def get_all_documents(self, collection_path: str):
        #Get all documents from a collection.
        collection_ref = self.db.collection(collection_path)
        return collection_ref.get()
    """
