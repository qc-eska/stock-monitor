import os
import requests

TOKEN = os.getenv("TELEGRAM_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
CHAT_ID = os.getenv("CHAT_ID")


def set_channel_photo(image_path):
    print("[PHOTO]", image_path)

    url = f"{BASE_URL}/setChatPhoto"

    try:
        with open(image_path, "rb") as photo:
            r = requests.post(
                url,
                data={"chat_id": CHAT_ID},
                files={"photo": photo}
            )
        print("[BRANDING PHOTO]", r.json())
        return r.json()
    except Exception as e:
        print("[ERROR PHOTO]", e)
        return None


def set_channel_title(title):
    print("[TITLE]", title)

    url = f"{BASE_URL}/setChatTitle"

    try:
        r = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "title": title
            }
        )
        print("[BRANDING TITLE]", r.json())
        return r.json()
    except Exception as e:
        print("[ERROR TITLE]", e)
        return None


def set_mode(mode):
    print("[MODE]", mode)

    mode = mode.lower()

    if mode in ["bullish", "green", "positive"]:
        set_channel_title("📈 JSW - WZROSTY")

    elif mode in ["bearish", "red", "negative"]:
        set_channel_title("📉 JSW - SPADKI")

    else:
        set_channel_title("⚖️ JSW - NEUTRAL")
