import time
import threading

from core.jsw import fetch_jsw_news
from core.impact_engine import filter_news
from telegram.bot import send_message


def news_loop():
    while True:
        print("TICK: fetching news...")

        news = fetch_jsw_news()

        alerts, mode = filter_news(news)

        # alerts → Telegram
        for alert in alerts:
            send_message(alert)

        time.sleep(300)  # 5 minut


def run():
    print("🚀 JSW CLEAN MONITOR STARTED")

    send_message("🚀 JSW MONITOR ONLINE")

    thread = threading.Thread(target=news_loop, daemon=True)
    thread.start()

    while True:
        time.sleep(60)


if __name__ == "__main__":
    run()
