import requests
import os

TOKEN = os.getenv("8523779434:AAEGSOgwR7LuQqXJlWlUmG4ZOj-YZLngoSQ")
CHAT_ID = os.getenv("-1003889107367")

def send_message(text):
    url = f"https://api.telegram.org/bot8523779434:AAEGSOgwR7LuQqXJlWlUmG4ZOj-YZLngoSQ/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text
    })
