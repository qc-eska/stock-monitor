import requests
import re

CACHE = {"price": None}

URL = "https://www.gpw.pl/spolka?isin=PLJSW0000015"


def extract_price(html):
    try:
        # GPW ma w HTML ostatnią cenę w formie liczby z przecinkiem
        match = re.search(r'kurs[^0-9]*([0-9]+,[0-9]+)', html.lower())

        if not match:
            return None

        price = float(match.group(1).replace(",", "."))

        return price

    except Exception as e:
        print("PARSE ERROR:", e)
        return None


def get_jsw_price():
    try:
        r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

        print("STATUS:", r.status_code)

        if r.status_code != 200:
            return fallback()

        price = extract_price(r.text)

        if price:
            CACHE["price"] = price
            return {"price": price, "currency": "PLN"}

        return fallback()

    except Exception as e:
        print("ERROR:", e)
        return fallback()


def fallback():
    if CACHE["price"]:
        print("USING CACHE:", CACHE["price"])
        return {"price": CACHE["price"], "currency": "PLN"}

    return None
