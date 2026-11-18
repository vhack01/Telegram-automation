"""
telegram_notifier.py — Send an urgent Telegram DM alert to the owner
"""

import logging
import httpx
from datetime import datetime
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_OWNER_CHAT_ID

logger = logging.getLogger(__name__)

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


async def send_alert(message_text: str = "") -> bool:
    """
    Send an urgent DM alert to the bot owner via Telegram.
    Returns True on success, False on failure.
    """
    try:
        now = datetime.now().strftime("%d %b %Y, %I:%M %p")

        alert = (
            "🚨 *ALERT — Your name was mentioned\\!*\n\n"
            f"📨 *Message:*\n_{escape(message_text[:300])}_\n\n"
            f"🕐 *Time:* {escape(now)}\n\n"
            "👉 Check your Telegram channel immediately\\!"
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{TELEGRAM_API}/sendMessage",
                json={
                    "chat_id": TELEGRAM_OWNER_CHAT_ID,
                    "text": alert,
                    "parse_mode": "MarkdownV2",
                },
                timeout=10,
            )

        data = response.json()
        if data.get("ok"):
            logger.info(f"✅ Alert DM sent to owner (chat_id={TELEGRAM_OWNER_CHAT_ID})")
            return True
        else:
            logger.error(f"❌ Telegram DM failed: {data}")
            return False

    except Exception as exc:
        logger.error(f"❌ Failed to send Telegram alert: {exc}")
        return False


def escape(text: str) -> str:
    """Escape special characters for Telegram MarkdownV2."""
    special = r"\_*[]()~`>#+-=|{}.!"
    return "".join(f"\\{c}" if c in special else c for c in text)
