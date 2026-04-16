import requests
import re

URL = "https://finance.yahoo.com/quote/JSW.WA"

CACHE = {"price": None}


def get_jsw_price():
    try:
        r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

        if r.status_code != 200:
            print("HTTP ERROR:", r.status_code)
            return None

        # szukamy konkretnego pola JSON embedded w HTML
        match = re.search(r'"regularMarketPrice":\{"raw":([0-9.]+)', r.text)

        if match:
            price = float(match.group(1))
            CACHE["price"] = price

            return {"price": price, "currency": "PLN"}

        if CACHE["price"]:
            return {"price": CACHE["price"], "currency": "PLN"}

        return None

    except Exception as e:
        print("ERROR:", e)
        return None
