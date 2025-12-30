import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

_db = None

def get_db():
    global _db

    if _db:
        return _db

    firebase_key = os.environ.get("FIREBASE_KEY")
    if not firebase_key:
        raise RuntimeError("FIREBASE_KEY not found")

    cred = credentials.Certificate(json.loads(firebase_key))

    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    _db = firestore.client()
    return _db
