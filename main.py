"""
main.py — FastAPI webhook server for Telegram bot
Listens for channel messages and sends a Telegram DM alert
when the name "Mantsa" is detected.
"""

import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse

from config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHANNEL_ID,
    TELEGRAM_OWNER_CHAT_ID,
    WATCH_NAMES,
    CALL_COOLDOWN_SECONDS,
    WEBHOOK_SECRET,
    PORT,
)
from telegram_notifier import send_alert

# ── Logging ───────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ── Cooldown tracker ──────────────────────────────────────
# Stores timestamp of the last call placed
_last_call_time: float = 0.0


def is_on_cooldown() -> bool:
    return (time.time() - _last_call_time) < CALL_COOLDOWN_SECONDS


def mark_call_sent() -> None:
    global _last_call_time
    _last_call_time = time.time()


# ── Name detection ────────────────────────────────────────
def contains_watch_name(text: str) -> bool:
    """Return True if any watched name appears in the message text."""
    lower = text.lower()
    return any(name in lower for name in WATCH_NAMES)


# ── FastAPI app ───────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🤖 Telegram Alert Bot starting up…")
    logger.info(f"👁  Watching for names: {WATCH_NAMES}")
    logger.info(f"📲 Will DM alert to chat_id: {TELEGRAM_OWNER_CHAT_ID}")
    logger.info(f"⏱  Cooldown between alerts: {CALL_COOLDOWN_SECONDS}s")
    yield
    logger.info("🛑 Bot shutting down.")


app = FastAPI(title="Telegram Call Bot", lifespan=lifespan)


@app.get("/")
async def health_check():
    """Simple health endpoint — Railway uses this to verify the app is alive."""
    return {"status": "ok", "watching_for": WATCH_NAMES}


@app.get("/twiml")
@app.post("/twiml")
async def twiml_response():
    """
    Twilio fetches this endpoint when the call connects.
    Returns TwiML XML that tells Twilio what to say.
    Works with Twilio trial accounts (no inline twiml param needed).
    """
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        "<Response>"
        "<Say>Alert! Your name Mantsa was mentioned in your Telegram channel. "
        "Please check your Telegram immediately.</Say>"
        "<Pause length=\"1\"/>"
        "<Say>Repeating. Your name Mantsa was mentioned in your Telegram channel. "
        "Please check your Telegram immediately.</Say>"
        "</Response>"
    )
    return Response(content=xml, media_type="application/xml")


@app.post("/webhook")
async def telegram_webhook(request: Request):
    """
    Telegram sends every channel update here via POST.
    We parse the message, check for the name, and call if found.
    """
    # ── Optional secret token check ───────────────────────
    if WEBHOOK_SECRET:
        token = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if token != WEBHOOK_SECRET:
            raise HTTPException(status_code=403, detail="Invalid secret token")

    # ── Parse body ────────────────────────────────────────
    try:
        update = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    logger.debug(f"Update received: {update}")

    # Telegram sends channel posts under "channel_post"
    # and edited channel posts under "edited_channel_post"
    post = update.get("channel_post") or update.get("edited_channel_post")

    if not post:
        # Not a channel post (maybe a private message, group, etc.) — ignore
        return Response(status_code=200)

    # ── Channel filter (optional) ─────────────────────────
    if TELEGRAM_CHANNEL_ID:
        chat_id = str(post.get("chat", {}).get("id", ""))
        if chat_id != TELEGRAM_CHANNEL_ID:
            logger.info(f"⏭  Ignored message from channel {chat_id} (not configured channel)")
            return Response(status_code=200)

    # ── Extract text ──────────────────────────────────────
    text = (
        post.get("text")
        or post.get("caption")  # For photos/videos with captions
        or ""
    )

    if not text:
        return Response(status_code=200)

    logger.info(f"📨 Channel message: {text[:100]}{'…' if len(text) > 100 else ''}")

    # ── Name detection ────────────────────────────────────
    if not contains_watch_name(text):
        logger.info("✅ No watched name found — no action needed.")
        return Response(status_code=200)

    logger.info(f"🚨 Name detected in message!")

    # ── Cooldown check ────────────────────────────────────
    if is_on_cooldown():
        remaining = int(CALL_COOLDOWN_SECONDS - (time.time() - _last_call_time))
        logger.info(f"⏳ On cooldown — skipping call ({remaining}s remaining).")
        return Response(status_code=200)

    # ── Place call ────────────────────────────────────────
    # Send a short preview of the message (first 100 chars)
    preview = text[:100]
    sent = await send_alert(message_text=text)

    if sent:
        mark_call_sent()
        logger.info(f"✅ Alert DM sent successfully!")
    else:
        logger.error("❌ Alert DM failed — check bot token and owner chat ID.")

    # Always return 200 to Telegram (so it doesn't retry)
    return Response(status_code=200)


# ── Run locally ───────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
