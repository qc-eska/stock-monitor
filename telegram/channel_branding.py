import os
import requests

TOKEN = os.getenv("TELEGRAM_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
CHAT_ID = os.getenv("CHAT_ID")


def set_channel_photo(image_path):
    print("[PHOTO]", image_path)

    url = f"{BASE_URL}/setChatPhoto"

    with open(image_path, "rb") as photo:
        r = requests.post(
            url,
            data={"chat_id": CHAT_ID},
            files={"photo": photo}
        )

    print("[BRANDING PHOTO]", r.json())
    return r.json()


def set_channel_title(title):
    print("[TITLE]", title)

    url = f"{BASE_URL}/setChatTitle"

    r = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "title": title
        }
    )

    print("[BRANDING TITLE]", r.json())
    return r.json()
