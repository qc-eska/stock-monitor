import time
from core.price_fetcher import get_jsw_price
from telegram.bot import send_message


def send_hourly_jsw_update():
    data = get_jsw_price()

    if not data:
        send_message("📊 JSW: brak danych rynkowych")
        return

    text = (
        f"📊 JSW UPDATE (1H)\n\n"
        f"Cena: {data['price']}\n"
        f"Zmiana: {data['change']} ({data['change_pct']}%)\n"
        f"Czas: {data['time']}"
    )

    send_message(text)
