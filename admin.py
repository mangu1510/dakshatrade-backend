from fastapi import APIRouter, Header, HTTPException
import os
from firebase_admin import firestore

router = APIRouter(prefix="/admin", tags=["Admin"])
db = firestore.client()

def verify_admin(x_admin_email: str):
    if x_admin_email != os.environ.get("ADMIN_EMAIL"):
        raise HTTPException(status_code=401, detail="Admin access denied")

# ---------------- USERS ----------------
@router.get("/users")
def get_users(x_admin_email: str = Header(None)):
    verify_admin(x_admin_email)
    users = []
    for doc in db.collection("users").stream():
        users.append(doc.to_dict())
    return users

# ---------------- SIGNALS ----------------
@router.get("/signals")
def get_signals(x_admin_email: str = Header(None)):
    verify_admin(x_admin_email)
    signals = []
    for doc in db.collection("signals").stream():
        data = doc.to_dict()
        data["id"] = doc.id
        signals.append(data)
    return signals

# ---------------- CLOSE SIGNAL (EMERGENCY) ----------------
@router.post("/close-signal/{signal_id}")
def close_signal(signal_id: str, x_admin_email: str = Header(None)):
    verify_admin(x_admin_email)
    db.collection("signals").document(signal_id).update({
        "status": "CLOSED"
    })
    return {"message": "Signal closed successfully"}
