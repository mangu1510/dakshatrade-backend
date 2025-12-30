from fastapi import APIRouter, Header, HTTPException
import os
from firebase_db import get_db

router = APIRouter(prefix="/admin", tags=["Admin"])
db = get_db()

def verify_admin(x_admin_email: str):
    if x_admin_email != os.environ.get("ADMIN_EMAIL"):
        raise HTTPException(status_code=401, detail="Admin access denied")

@router.get("/users")
def get_users(x_admin_email: str = Header(None)):
    verify_admin(x_admin_email)
    return [doc.to_dict() for doc in db.collection("users").stream()]

@router.get("/signals")
def get_signals(x_admin_email: str = Header(None)):
    verify_admin(x_admin_email)
    data = []
    for doc in db.collection("signals").stream():
        d = doc.to_dict()
        d["id"] = doc.id
        data.append(d)
    return data

@router.post("/close-signal/{signal_id}")
def close_signal(signal_id: str, x_admin_email: str = Header(None)):
    verify_admin(x_admin_email)
    db.collection("signals").document(signal_id).update({
        "status": "CLOSED"
    })
    return {"message": "Signal closed"}
