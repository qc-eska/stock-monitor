import time
from datetime import datetime
from zoneinfo import ZoneInfo

from config import HOURLY_REPORT_INTERVAL, PRICE_ALERT_THRESHOLD_PERCENT
from database.db import get_state, set_state


LAST_HOURLY_REPORT_AT = "last_hourly_report_at"
PRICE_ALERT_ANCHOR = "price_alert_anchor"
MARKET_TIMEZONE = ZoneInfo("Europe/Warsaw")


def format_price(value):
    return f"{value:.2f}".replace(".", ",")


def is_market_open(now=None):
    current_time = now or datetime.now(MARKET_TIMEZONE)

    if current_time.weekday() >= 5:
        return False

    minutes = current_time.hour * 60 + current_time.minute
    market_open = 9 * 60
    market_close = 16 * 60 + 50

    return market_open <= minutes <= market_close


def send_hourly_report(quote, send_message):
    message = (
        "🕐 JSW raport godzinowy\n"
        f"Kurs: {format_price(quote['price'])} zł\n"
        f"Zmiana dnia: {quote['change_percent']:+.2f}%\n"
        f"Czas notowania: {quote['timestamp']}\n"
        f"{quote['url']}"
    )
    send_message(message)
    set_state(LAST_HOURLY_REPORT_AT, int(time.time()))


def send_threshold_alert(quote, percent_change, send_message):
    direction = "w górę" if percent_change > 0 else "w dół"
    emoji = "📈" if percent_change > 0 else "📉"
    message = (
        f"{emoji} JSW zmiana o {abs(percent_change):.2f}% {direction}\n"
        f"Kurs: {format_price(quote['price'])} zł\n"
        f"Zmiana dnia: {quote['change_percent']:+.2f}%\n"
        f"Czas notowania: {quote['timestamp']}\n"
        f"{quote['url']}"
    )
    send_message(message)
    set_state(PRICE_ALERT_ANCHOR, quote["price"])


def process_quote(quote, send_message):
    if not is_market_open():
        return

    now = int(time.time())
    last_hourly_report_at = int(get_state(LAST_HOURLY_REPORT_AT, "0"))
    anchor_raw = get_state(PRICE_ALERT_ANCHOR)

    if now - last_hourly_report_at >= HOURLY_REPORT_INTERVAL:
        send_hourly_report(quote, send_message)

    if anchor_raw is None:
        set_state(PRICE_ALERT_ANCHOR, quote["price"])
        return

    anchor_price = float(anchor_raw)
    if anchor_price <= 0:
        set_state(PRICE_ALERT_ANCHOR, quote["price"])
        return

    percent_change = ((quote["price"] - anchor_price) / anchor_price) * 100
    if abs(percent_change) >= PRICE_ALERT_THRESHOLD_PERCENT:
        send_threshold_alert(quote, percent_change, send_message)
