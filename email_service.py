"""Send portfolio contact notifications through Resend's HTTPS API.

Drop this file in place of the existing email_service.py. It keeps the
send_contact_email() interface used by routes.py and uses only Python's
standard library, so no new package is required.
"""

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv

load_dotenv()

RESEND_API_URL = "https://api.resend.com/emails"
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
NOTIFY_TO = os.getenv("NOTIFY_TO")
EMAIL_FROM = os.getenv("EMAIL_FROM", "onboarding@resend.dev")


def send_contact_email(name: str, email: str, subject: str, message: str) -> None:
    """Send a contact-form notification; failures are logged for Render."""
    if not RESEND_API_KEY:
        print("[EMAIL ERROR] RESEND_API_KEY is not configured")
        return
    if not NOTIFY_TO:
        print("[EMAIL ERROR] NOTIFY_TO is not configured")
        return

    payload = {
        "from": EMAIL_FROM,
        "to": [NOTIFY_TO],
        "reply_to": email,
        "subject": f"[Portfolio] {subject.strip()}",
        "text": (
            "New message from your portfolio\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Subject: {subject}\n\n"
            f"{message}"
        ),
    }
    request = Request(
        RESEND_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=15) as response:
            response_body = response.read().decode("utf-8")
            if response.status not in (200, 201):
                print(f"[EMAIL ERROR] Resend returned HTTP {response.status}: {response_body}")
                return
            print(f"[EMAIL] Notification accepted by Resend: {response_body}")
    except HTTPError as err:
        details = err.read().decode("utf-8", errors="replace")
        print(f"[EMAIL ERROR] Resend returned HTTP {err.code}: {details}")
    except (URLError, TimeoutError, OSError) as err:
        print(f"[EMAIL ERROR] Could not reach Resend API: {err}")
