from core.jsw import fetch_jsw_news
from core.news_filter import process_news
from telegram.channel_branding import set_mode

def run_cycle():
    print("TICK: fetching news...")

    articles = fetch_jsw_news()

    for article in articles:
        result = process_news(article)

        if not result:
            continue

        print("[SEND]", result["message"])

        # 👇 Twoja funkcja wysyłki
        send_to_telegram(result["message"])

        # 👇 zmiana trybu kanału
        set_mode(result["mode"])
