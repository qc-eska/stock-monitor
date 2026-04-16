import time
from core.jsw import fetch_jsw_news, analyze
from telegram.bot import send_message

def run():

    send_message("📡 JSW monitor START")

    while True:
        try:
            news = fetch_jsw_news()
            alerts = analyze(news)

            for a in alerts:
                send_message(a)

            print("scan ok:", len(news))

        except Exception as e:
            send_message(f"ERROR JSW: {e}")

        time.sleep(600)  # co 10 min


if __name__ == "__main__":
    run()
