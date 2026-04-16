import requests

TOKEN = "TWOJ_TOKEN"

def send_alert(text, chat_id):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": chat_id,
        "text": text
    })
