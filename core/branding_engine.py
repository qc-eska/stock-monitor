import os
from telegram.channel_branding import set_channel_photo, set_channel_title

STATE = {"mode": "green"}

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MODES = {
    "green": {
        "title": "JSW Monitor 🟢",
        "photo": os.path.join(BASE_DIR, "assets/green.jpg")
    },
    "yellow": {
        "title": "JSW Monitor 🟡 ALERT",
        "photo": os.path.join(BASE_DIR, "assets/yellow.jpg")
    },
    "red": {
        "title": "JSW MONITOR 🔴 PANIC",
        "photo": os.path.join(BASE_DIR, "assets/red.jpg")
    }
}


def set_mode(mode):
    if mode not in MODES:
        return

    if STATE["mode"] == mode:
        return

    config = MODES[mode]

    try:
        set_channel_title(config["title"])
        set_channel_photo(config["photo"])
    except Exception as e:
        print("[BRANDING ERROR]", e)
        return

    STATE["mode"] = mode
    print(f"[BRANDING] set mode: {mode}")
