# main.py

import time
from core.jsw import fetch_jsw_news
from core.impact_engine import filter_news
from telegram.bot import send_message

def run():

    send_message("📡 JSW IMPACT MONITOR START")

    while True:
        try:
            news = fetch_jsw_news()

            alerts = filter_news(news)

            if alerts:
                for a in alerts:
                    send_message(a)
            else:
                print("no high impact news")

            print("scan ok:", len(news))

        except Exception as e:
            send_message(f"ERROR JSW: {e}")

        time.sleep(600)


if __name__ == "__main__":
    run()
