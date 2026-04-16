import requests
import re

CACHE = {"price": None}

URL = "https://www.gpw.pl/spolka?isin=PLJSW0000015"


def extract_price(html):
    try:
        # szukamy liczby typu 27,25 lub 27.25
        match = re.search(r'([0-9]{1,3}[.,][0-9]{2})', html)

        if not match:
            return None

        price = float(match.group(1).replace(",", "."))

        # sanity check (JSW nie może być 300+)
        if price < 1 or price > 200:
            return None

        return price

    except:
        return None


def get_jsw_price():
    try:
        r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

        if r.status_code != 200:
            return fallback()

        price = extract_price(r.text)

        if price:
            CACHE["price"] = price
            return {"price": price, "currency": "PLN"}

        return fallback()

    except:
        return fallback()


def fallback():
    if CACHE["price"]:
        return {"price": CACHE["price"], "currency": "PLN"}

    return None
