import requests
import time

CACHE = {
    "price": None,
    "timestamp": 0
}

URL = "https://query1.finance.yahoo.com/v8/finance/chart/JSW.WA"


def fetch_live():
    r = requests.get(URL, timeout=10)
    data = r.json()

    return data["chart"]["result"][0]["meta"]["regularMarketPrice"]


def get_jsw_price():
    now = time.time()

    # 🧠 cache 10 minut
    if CACHE["price"] and now - CACHE["timestamp"] < 600:
        return {"price": CACHE["price"]}

    try:
        price = fetch_live()

        CACHE["price"] = float(price)
        CACHE["timestamp"] = now

        return {"price": CACHE["price"]}

    except
