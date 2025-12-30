from fastapi import FastAPI, Request, HTTPException
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

app = FastAPI(title="DakshaTrade Backend")

# ---------------- FIREBASE INIT ----------------
firebase_key = os.environ.get("FIREBASE_KEY")

if not firebase_key:
    raise RuntimeError("Firebase key not found")

cred = credentials.Certificate(json.loads(firebase_key))
firebase_admin.initialize_app(cred)
db = firestore.client()

# ---------------- HEALTH CHECK ----------------
@app.get("/")
def health():
    return {"status": "DakshaTrade backend running"}

# ---------------- TRADINGVIEW WEBHOOK ----------------
@app.post("/webhook")
async def tradingview_webhook(request: Request):
    secret = request.headers.get("X-SECRET")

    if secret != os.environ.get("WEBHOOK_SECRET"):
        raise HTTPException(status_code=401, detail="Unauthorized")

    data = await request.json()

    db.collection("signals").add({
        "strategy_id": data["strategy"],
        "symbol": data["symbol"],
        "side": data["side"],
        "price": float(data["price"]),
        "time": data["time"],
        "status": "OPEN"
    })

    return {"message": "Signal received"}
