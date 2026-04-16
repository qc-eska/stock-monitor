import time
import threading

from core.price_fetcher import get_jsw_price
from telegram.bot import send_message


def test_loop():
    while True:
        print("TICK: checking price...")

        data = get_jsw_price()

        print("PRICE RESULT:", data)

        if data:
            send_message(f"📊 JSW TEST: {data['price']}")

        time.sleep(30)


def run():
    print("🚀 JSW MONITOR STARTED")

    send_message("🚀 JSW MONITOR ONLINE")

    thread = threading.Thread(target=test_loop, daemon=True)
    thread.start()

    while True:
        time.sleep(60)


if __name__ == "__main__":
    run()
