from core.price_state import STATE
from telegram.bot import send_message


ALERT_THRESHOLD = 1.0


def send_hourly_jsw_update(price_data):
    if not price_data:
        return

    price = price_data["price"]

    if STATE["last_report_price"] is None:
        STATE["last_report_price"] = price
        STATE["reference_price"] = price
        return

    change_1h = ((price - STATE["last_report_price"]) / STATE["last_report_price"]) * 100
    STATE["last_report_price"] = price

    send_message(
        f"📊 JSW REPORT (1H)\n\n"
        f"Cena: {price} PLN\n"
        f"Zmiana 1h: {change_1h:+.2f}%"
    )

    ref = STATE["reference_price"]
    change = ((price - ref) / ref) * 100

    if abs(change) >= ALERT_THRESHOLD:
        send_message(
            f"🚨 JSW ALERT ±1%\n\n"
            f"Cena: {price} PLN\n"
            f"Ruch: {change:+.2f}%"
        )

        STATE["reference_price"] = price
