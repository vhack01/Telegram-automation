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
    APP_URL,
)

logger = logging.getLogger(__name__)


def place_call(message_preview: str = ""):
    """
    Place a call to YOUR_PHONE_NUMBER.
    Uses APP_URL/twiml as the TwiML source (works with Twilio trial accounts).
    Returns the Twilio call SID on success, None on failure.
    """
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        # Use our own /twiml endpoint — works on Twilio trial accounts
        twiml_url = f"{APP_URL}/twiml"
        logger.info(f"📡 Using TwiML URL: {twiml_url}")

        call = client.calls.create(
            to=YOUR_PHONE_NUMBER,
            from_=TWILIO_FROM_NUMBER,
            url=twiml_url,   # <-- url instead of twiml param
        )

        logger.info(f"📞 Call placed! SID={call.sid} → {YOUR_PHONE_NUMBER}")
        return call.sid

    except Exception as exc:
        logger.error(f"❌ Failed to place call: {exc}")
        return None
