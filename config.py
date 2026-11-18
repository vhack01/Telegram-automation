"""
config.py — Load all environment variables from .env
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Telegram ──────────────────────────────────────────────
TELEGRAM_BOT_TOKEN: str = os.environ["TELEGRAM_BOT_TOKEN"]
# Optional: restrict webhook to only your channel (channel ID as negative int)
TELEGRAM_CHANNEL_ID: str = os.getenv("TELEGRAM_CHANNEL_ID", "")
# Your personal Telegram chat ID — bot will DM you here when alert fires
TELEGRAM_OWNER_CHAT_ID: str = os.environ["TELEGRAM_OWNER_CHAT_ID"]

# ── Twilio ────────────────────────────────────────────────
TWILIO_ACCOUNT_SID: str = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN: str = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_FROM_NUMBER: str = os.environ["TWILIO_FROM_NUMBER"]   # e.g. +1XXXXXXXXXX

# ── Alert target ──────────────────────────────────────────
YOUR_PHONE_NUMBER: str = os.getenv("YOUR_PHONE_NUMBER", "+919569288612")

# ── Detection ─────────────────────────────────────────────
# Name(s) to watch for — comma-separated for multiple names
WATCH_NAMES: list[str] = [
    n.strip().lower()
    for n in os.getenv("WATCH_NAMES", "Mantsa").split(",")
    if n.strip()
]

# Cooldown in seconds between calls (default 5 min)
# Prevents flooding if many messages arrive at once
CALL_COOLDOWN_SECONDS: int = int(os.getenv("CALL_COOLDOWN_SECONDS", "300"))

# ── Server ────────────────────────────────────────────────
PORT: int = int(os.getenv("PORT", "8000"))

# Your Railway public URL (e.g. https://xxxx.up.railway.app)
# Used so Twilio can fetch the TwiML message from our app
APP_URL: str = os.getenv("APP_URL", "").rstrip("/")

# ── Webhook secret (optional extra security) ───────────────
WEBHOOK_SECRET: str = os.getenv("WEBHOOK_SECRET", "")
