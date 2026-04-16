import os
import requests

TOKEN = os.getenv("TELEGRAM_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
CHAT_ID = os.getenv("CHAT_ID")

CURRENT_MODE = None

# 🔥 priorytet trybów
PRIORITY = {
    "bullish": 1,
    "neutral": 0,
    "bearish": 2
}


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

    # 🔥 jeśli pierwszy raz
    if CURRENT_MODE is None:
        CURRENT_MODE = mode

    # 🔥 jeśli nowy jest słabszy → ignoruj
    elif PRIORITY.get(mode, 0) < PRIORITY.get(CURRENT_MODE, 0):
        print("[SKIP] weaker signal")
        return

    # 🔥 jeśli taki sam → ignoruj
    elif mode == CURRENT_MODE:
        print("[SKIP] mode unchanged")
        return

    CURRENT_MODE = mode

    if mode == "bullish":
        set_channel_title("📈 JSW - WZROSTY")

    elif mode == "bearish":
        set_channel_title("📉 JSW - SPADKI")

    else:
        set_channel_title("⚖️ JSW - NEUTRAL")
