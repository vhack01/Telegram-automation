"""
twilio_caller.py — Place a phone call via Twilio Voice API
"""

import logging
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_FROM_NUMBER,
    YOUR_PHONE_NUMBER,
)

logger = logging.getLogger(__name__)


def build_twiml(message_preview: str = "") -> str:
    """
    Build the TwiML XML that Twilio will read aloud when you pick up.
    """
    response = VoiceResponse()

    alert_text = (
        "Hello! This is an automated alert. "
        "Your name, Mantsa, was just mentioned in your Telegram channel. "
    )
    if message_preview:
        alert_text += f"The message said: {message_preview}. "
    alert_text += "Please check your Telegram immediately. Goodbye!"

    # Repeat the message twice so you don't miss it
    response.say(alert_text, voice="Polly.Joanna", language="en-US")
    response.pause(length=1)
    response.say("Repeating: " + alert_text, voice="Polly.Joanna", language="en-US")

    return str(response)


def place_call(message_preview: str = "") -> str | None:
    """
    Place a call to YOUR_PHONE_NUMBER.
    Returns the Twilio call SID on success, None on failure.
    """
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        twiml = build_twiml(message_preview)

        call = client.calls.create(
            to=YOUR_PHONE_NUMBER,
            from_=TWILIO_FROM_NUMBER,
            twiml=twiml,
            # Optional: timeout after 30 seconds of ringing
            timeout=30,
        )

        logger.info(f"📞 Call placed! SID={call.sid} → {YOUR_PHONE_NUMBER}")
        return call.sid

    except Exception as exc:
        logger.error(f"❌ Failed to place call: {exc}")
        return None
