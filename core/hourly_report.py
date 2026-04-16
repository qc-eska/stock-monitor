from core.price_fetcher import get_jsw_price
from core.price_state import STATE
from telegram.bot import send_message


THRESHOLD = 1.0  # 1%


def send_hourly_jsw_update():
    data = get_jsw_price()

    if not data:
        return

    price = data["price"]

    last_price = STATE["last_price"]

    # pierwsze uruchomienie
    if last_price is None:
        STATE["last_price"] = price
        return

    change_pct = ((price - last_price) / last_price) * 100

    # aktualizacja stanu zawsze
    STATE["last_price"] = price

    # alert tylko przy ruchu >= 1%
    if abs(change_pct) >= THRESHOLD:

        direction = "📈" if change_pct > 0 else "📉"

        text = (
            f"{direction} JSW MOVE ALERT (±1%)\n\n"
            f"Cena: {price}\n"
            f"Zmiana: {change_pct:.2f}%\n"
            f"Czas: {data['time']}"
        )

        send_message(text)
