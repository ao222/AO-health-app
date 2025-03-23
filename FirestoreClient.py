import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, firestore

import util_time


#    credentials obtained through the streamlit community
#    st secrets toml file. The toml file must have a [firebase]
#    section formatted as follows:
    
#    [firebase]
#    type = "service_account"
#    project_id = "XXX"
#    private_key_id = "XXX"
#    private_key = "XXX"
#    client_email = "XXX"
#    client_id = "XXX"
#    auth_uri = "https://accounts.google.com/o/oauth2/auth"
#    token_uri = "https://oauth2.googleapis.com/token"
#    auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
#    client_x509_cert_url = "XXX"
    
#    The values may be obtained through creating a json credentials file
#    from the firestore console.


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

    def save_food_snapshot(self, description, calories):
        user_id = "user_123"
        # timestamp = util_time.now()
        timestamp = datetime.utcnow().isoformat()
        
        data = {
            "description": description,
            "calories": calories,
            "timestamp": timestamp
        }

        # Save data to Firestore
        self.db.collection("users").document(user_id).collection("foods").document(timestamp).set(data)
    
    def save_subjective_snapshot(self, motivation, restfulness, irritability, social_energy, levity, productivity, appetite, psychosis, depression, mania):
        user_id = "user_123"
        timestamp = datetime.utcnow().isoformat()
        data = {
            "motivation": motivation,
            "restfulness": restfulness,
            "irritability": irritability,
            "social_energy": social_energy,
            "levity": levity,
            "productivity": productivity,
            "appetite": appetite,
            "psychosis": psychosis,
            "depression": depression,
            "mania": mania,
            "timestamp": timestamp
        }

        # Save data to Firestore
        self.db.collection("users").document(user_id).collection("subjectives").document(timestamp).set(data)
    
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

    def save_daily_snapshot(self, sleep_hours, naps, walking_minutes, lifting_minutes, calories, caffeine):
        user_id = "user_123"
        today = util_time.get_today_timestamp()
        data = {
            "date": today,
            "sleep_hours": sleep_hours,
            "naps": naps,
            "walking_minutes": walking_minutes,
            "lifting_minutes": lifting_minutes,
            "calories": calories,
            "caffeine": caffeine
        }

        # Save data to Firestore
        self.db.collection("users").document(user_id).collection("dailies").document(today).set(data)

    def get_daily_snapshot(self):
        user_id = "user_123"
        today = util_time.get_today_timestamp()
    
        # Retrieve data from Firestore
        doc_ref = self.db.collection("users").document(user_id).collection("dailies").document(today)
        doc = doc_ref.get()
    
        if doc.exists:
            return doc.to_dict()
        else:
            return None

    def get_all_objective_snapshots(self):
        objective_snapshot_ref = self.db.collection("users").document("user_123").collection("objectives")
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
            
    def get_food_snapshots(self,from_timestamp, to_timestamp):
        user_id = "user_123"
        start_time_str = from_timestamp.replace(tzinfo=None).isoformat(timespec="microseconds")
        end_time_str = to_timestamp.replace(tzinfo=None).isoformat(timespec="microseconds")
        
        # Reference Firestore objectives collection
        food_snapshot_ref = self.db.collection("users").document("user_123").collection("foods")
        print(start_time_str)
        print(end_time_str)
        # Query Firestore using document IDs (which are ISO formatted timestamps)
        query = (
            food_snapshot_ref
            .order_by("__name__")  # Query based on document ID
            .start_at(start_time_str)  # Start at documents created at or after start_time
            .end_at(end_time_str)  # End at documents created at or before end_time
        )

        # debug code:
        print(f"Querying Firestore from {start_time_str} to {end_time_str}")
        
        # Execute query and fetch documents
        docs = query.stream()

        # Debugging: Check if the query result is empty
        docs_list = list(docs)  # Convert iterator to list for debugging
        print(f"Number of documents found: {len(docs_list)}")
        
        # Process Results
        data = []
        for doc in docs:
            doc_data = doc.to_dict()
            data.append({
                "timestamp": doc_data.get("timestamp"),
                "description": doc_data.get("description"),
                "calories": doc_data.get("calories")
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

    def delete_food_item(self, timestamp):
        user_id = "user_123"
        
        doc_ref = self.db.collection("users").document(user_id).collection("foods").document(timestamp)
        doc_ref.delete()
