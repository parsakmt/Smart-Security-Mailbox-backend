import firebase_admin
from firebase_admin import messaging, credentials
import os
from dotenv import load_dotenv

load_dotenv()


def send_to_token(device_tokens):
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.getenv("FIREBASE_MESSAING_CRED"))
        firebase_admin.initialize_app(cred)

    # See documentation on defining a message payload.
    message = messaging.MulticastMessage(
        data={"title": "Hello,", "body": "You have mail!"},
        tokens=device_tokens,
        android=messaging.AndroidConfig(priority="high"),
    )
    messaging.send_multicast(message)
