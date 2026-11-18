"""
twilio_caller.py — Place a phone call via Twilio Voice API
"""

import logging
from twilio.rest import Client
from config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_FROM_NUMBER,
    YOUR_PHONE_NUMBER,
)

logger = logging.getLogger(__name__)


def place_call(message_preview: str = ""):
    """
    Place a call to YOUR_PHONE_NUMBER.
    Returns the Twilio call SID on success, None on failure.
    """
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        # Simplest possible TwiML — works on all Twilio trial accounts
        twiml = (
            "<Response>"
            "<Say>Alert! Your name Mantsa was mentioned in your Telegram channel. "
            "Please check your Telegram immediately.</Say>"
            "</Response>"
        )

        call = client.calls.create(
            to=YOUR_PHONE_NUMBER,
            from_=TWILIO_FROM_NUMBER,
            twiml=twiml,
        )

        logger.info(f"📞 Call placed! SID={call.sid} → {YOUR_PHONE_NUMBER}")
        return call.sid

    except Exception as exc:
        logger.error(f"❌ Failed to place call: {exc}")
        return None
