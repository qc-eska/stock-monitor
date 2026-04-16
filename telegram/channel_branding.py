import os
import requests

TOKEN = os.getenv("TELEGRAM_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
CHAT_ID = os.getenv("CHAT_ID")

CURRENT_MODE = None  # 🔥 pamięta ostatni stan


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
    except Exception as e:
        print("[ERROR TITLE]", e)


def set_mode(mode):
    global CURRENT_MODE

    print("[MODE]", mode)

    mode = mode.lower()

    # 🔥 NIE zmieniaj jeśli to samo
    if mode == CURRENT_MODE:
        print("[SKIP] mode unchanged")
        return

    CURRENT_MODE = mode

    if mode in ["bullish", "green", "positive"]:
        set_channel_title("📈 JSW - WZROSTY")

    elif mode in ["bearish", "red", "negative"]:
        set_channel_title("📉 JSW - SPADKI")

    else:
        set_channel_title("⚖️ JSW - NEUTRAL")
