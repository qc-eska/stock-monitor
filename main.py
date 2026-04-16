import time
import threading

from core.hourly_report import send_hourly_jsw_update
from telegram.bot import send_message


# ----------------------------
# 🕐 PRICE LOOP (±1% alert inside module)
# ----------------------------
def hourly_loop():
    while True:
        try:
            send_hourly_jsw_update()
        except Exception as e:
            print("Hourly error:", e)

        time.sleep(3600)


# ----------------------------
# 🚀 MAIN
# ----------------------------
def run():
    send_message("📊 JSW MONITOR STARTED (CLEAN MODE)")

    while True:
        try:
            # tu możesz później dodać news engine
            print("JSW monitor running...")

        except Exception as e:
            print("ERROR:", e)
            send_message(f"⚠️ ERROR: {e}")

        time.sleep(60)


if __name__ == "__main__":
    threading.Thread(target=hourly_loop, daemon=True).start()
    run()
