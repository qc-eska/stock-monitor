import requests
import time

CACHE = {
    "price": None,
    "ts": 0
}

# Stooq (najstabilniejsze, mimo opóźnień)
URL = "https://stooq.pl/q/l/?s=jsw_pl&i=1"


def fetch_price():
    r = requests.get(URL, timeout=10)

    if r.status_code != 200:
        print("HTTP ERROR:", r.status_code)
        return None

    lines = r.text.strip().split("\n")

    if len(lines) < 2:
        return None

    row = lines[1].split(",")

    try:
        # Close price
        price = float(row[4])
        return price
    except:
        return None


def get_jsw_price():
    now = time.time()

    # 🧠 cache 5 min
    if CACHE["price"] and now - CACHE["ts"] < 300:
        return {"price": CACHE["price"]}

    price = fetch_price()

    if price:
        CACHE["price"] = price
        CACHE["ts"] = now
        return {"price": price}

    # fallback: jeśli wszystko padło → ostatnia znana cena
    if CACHE["price"]:
        print("USING STALE CACHE")
        return {"price": CACHE["price"]}

    return None
