import time
import threading

from core.price_fetcher import get_jsw_price
from telegram.bot import send_message


STATE = {
    "reference_price": None
}


# ----------------------------
# 🟢 START REPORT
# ----------------------------
def send_start_price():
    data = get_jsw_price()

    if not data:
        send_message("📊 JSW START: brak danych")
        return

    price = data["price"]
    STATE["reference_price"] = price

    send_message(
        f"📊 JSW START\n\nCena: {price}"
    )


# ----------------------------
# 🕐 HOURLY REPORT (STAŁY)
# ----------------------------
def hourly_loop():
    while True:
        data = get_jsw_price()

        if data:
            send_message(
                f"📊 JSW HOURLY\n\nCena: {data['price']}"
            )

        time.sleep(3600)


# ----------------------------
# 🚨 REAL-TIME ALERT LOOP
# ----------------------------
def alert_loop():
    while True:
        data = get_jsw_price()

        if data and STATE["reference_price"]:
            price = data["price"]
            ref = STATE["reference_price"]

            change = ((price - ref) / ref) * 100

            if abs(change) >= 1.0:

                direction = "📈" if change > 0 else "📉"

                send_message(
                    f"{direction} JSW ALERT (±1%)\n\n"
                    f"Cena: {price}\n"
                    f"Ruch: {change:+.2f}%"
                )

                # reset bazy po triggerze
                STATE["reference_price"] = price

        time.sleep(180)  # 3 minuty check


# ----------------------------
# 🚀 MAIN
# ----------------------------
def run():
    send_message("🚀 JSW MONITOR ONLINE (START + HOURLY + ALERTS)")

    send_start_price()

    threading.Thread(target=hourly_loop, daemon=True).start()
    threading.Thread(target=alert_loop, daemon=True).start()

    while True:
        time.sleep(60)


if __name__ == "__main__":
    run()
