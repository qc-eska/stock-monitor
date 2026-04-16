import time
import requests
import os

from core.jsw import fetch_jsw_news
from core.news_filter import process_news
from telegram.channel_branding import set_mode

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"


def send_to_telegram(message):
    url = f"{BASE_URL}/sendMessage"

    try:
        r = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "text": message,
                "disable_web_page_preview": False
            }
        )
        print("[TELEGRAM]", r.json())
    except Exception as e:
        print("[ERROR TELEGRAM]", e)


def run_cycle():
    print("TICK: fetching news...")

    articles = fetch_jsw_news()

    print("[DEBUG] RAW ARTICLES:", articles)
    print(f"[FOUND] {len(articles)} articles")

    for article in articles:
        print("[DEBUG] ARTICLE:", article)

        result = process_news(article)

        print("[DEBUG] RESULT:", result)

        if not result:
            continue

        message = result["message"]

        print("[SEND]", message)

        send_to_telegram(message)
        set_mode(result["mode"])


def main():
    print("🚀 JSW CLEAN MONITOR STARTED")

    while True:
        try:
            run_cycle()
        except Exception as e:
            print("[ERROR MAIN LOOP]", e)

        time.sleep(300)


if __name__ == "__main__":
    main()
