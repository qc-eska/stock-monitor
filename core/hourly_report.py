from core.price_fetcher import get_jsw_price
from core.price_state import STATE
from telegram.bot import send_message


ALERT_THRESHOLD = 1.0  # 1%


def send_hourly_jsw_update():
    data = get_jsw_price()

    if not data:
        return

    price = data["price"]

    # ----------------------------
    # 🕐 INIT STATE
    # ----------------------------
    if STATE["last_report_price"] is None:
        STATE["last_report_price"] = price
        STATE["reference_price"] = price
        return

    # ----------------------------
    # 📊 HOURLY REPORT (always)
    # ----------------------------
    report_change = ((price - STATE["last_report_price"]) / STATE["last_report_price"]) * 100

    STATE["last_report_price"] = price

    report = (
        f"📊 JSW REPORT (1H)\n\n"
        f"Cena: {price}\n"
        f"Zmiana 1h: {report_change:+.2f}%\n"
        f"Czas: {data['time']}"
    )

    send_message(report)

    # ----------------------------
    # 🚨 ALERT SYSTEM (±1%)
    # ----------------------------
    ref = STATE["reference_price"]
    change_from_ref = ((price - ref) / ref) * 100

    if abs(change_from_ref) >= ALERT_THRESHOLD:

        direction = "📈" if change_from_ref > 0 else "📉"

        alert = (
            f"{direction} JSW ALERT (±1%)\n\n"
            f"Cena: {price}\n"
            f"Ruch: {change_from_ref:+.2f}%\n"
            f"Czas: {data['time']}"
        )

        send_message(alert)

        # reset reference po triggerze
        STATE["reference_price"] = price
