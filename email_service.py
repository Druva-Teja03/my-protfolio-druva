import os, smtplib, ssl
from email.message import EmailMessage 
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD= os.getenv("SMTP_PASSWORD")
NOTIFY_TO = os.getenv("NOTIFY_TO", SMTP_USER)

def send_contact_email(name, email, subject, message):
    if not (SMTP_USER and SMTP_PASSWORD):
        print("[EMAIL] Not configured, skipping")
        return
    try:
        msg = EmailMessage()
        msg["Subject"] = "[Portfolio]" + " ".join(subject.split())
        msg["From"] = SMTP_USER
        msg["To"] = NOTIFY_TO
        msg["Reply-To"] = email          # pressing Reply goes to the visitor
        msg.set_content(
            f"New message from your portfolio\n\n"
            f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\n{message}"
        )
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT,
                              context=ssl.create_default_context(), timeout=15) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as err:
        print(f"[EMAIL ERROR] {err}")
