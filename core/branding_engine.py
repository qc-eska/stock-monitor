from telegram.channel_branding import set_channel_photo, set_channel_title

STATE = {
    "mode": "green"
}


MODES = {
    "green": {
        "title": "JSW Monitor 🟢",
        "photo": "assets/green.jpg"
    },
    "yellow": {
        "title": "JSW Monitor 🟡 ALERT",
        "photo": "assets/yellow.jpg"
    },
    "red": {
        "title": "JSW MONITOR 🔴 PANIC",
        "photo": "assets/red.jpg"
    }
}


def set_mode(mode):
    if mode not in MODES:
        return

    config = MODES[mode]

    set_channel_title(config["title"])
    set_channel_photo(config["photo"])

    STATE["mode"] = mode

    print(f"[BRANDING] set mode: {mode}")
