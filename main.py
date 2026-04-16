import time
import threading

from core.jsw import fetch_jsw_news
from core.impact_engine import filter_news
from telegram.bot import send_message


def news_loop():
    while True:
        print("TICK: fetching news...")

        news = fetch_jsw_news()
        alerts = filter_news(news)

        for a in alerts:
            send_message(a)

        time.sleep(300)  # 5 min


def run():
    print("🚀 JSW NEWS MONITOR STARTED")

    send_message("🚀 JSW NEWS MONITOR ONLINE")

    t = threading.Thread(target=news_loop, daemon=True)
    t.start()

    while True:
        time.sleep(60)


if __name__ == "__main__":
    run()
