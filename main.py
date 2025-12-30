from fastapi import FastAPI, Request, HTTPException
import os
from firebase_db import get_db
from admin import router as admin_router

app = FastAPI(title="DakshaTrade Backend")
app.include_router(admin_router)

db = get_db()

@app.get("/")
def health():
    return {"status": "DakshaTrade backend running"}

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
