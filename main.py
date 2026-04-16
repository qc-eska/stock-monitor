import time
import threading

from core.price_fetcher import get_jsw_price
from core.hourly_report import send_hourly_jsw_update
from core.jsw import fetch_jsw_news
from telegram.bot import send_message


def price_loop():
    while True:
        print("TICK: checking price...")

        price = get_jsw_price()
        print("PRICE:", price)

        send_hourly_jsw_update(price)

        time.sleep(60)


def news_loop():
    while True:
        news = fetch_jsw_news()

        if news:
            print("NEWS COUNT:", len(news))

        time.sleep(300)


def run():
    print("🚀 JSW MONITOR STARTED")

    send_message("🚀 JSW MONITOR ONLINE")

    threading.Thread(target=price_loop, daemon=True).start()
    threading.Thread(target=news_loop, daemon=True).start()

    while True:
        time.sleep(60)


if __name__ == "__main__":
    run()
