import requests
import re

CACHE = {
    "price": None
}


URL = "https://finance.yahoo.com/quote/JSW.WA"


def get_price_from_html(html):
    match = re.search(r'"regularMarketPrice":\{"raw":([0-9.]+)', html)
    if match:
        return float(match.group(1))
    return None


def get_jsw_price():
    try:
        r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

        print("STATUS:", r.status_code)

        if r.status_code != 200:
            return None

        price = get_price_from_html(r.text)

        if price:
            CACHE["price"] = price
            return {"price": price}

        if CACHE["price"]:
            print("USING CACHE")
            return {"price": CACHE["price"]}

        return None

    except Exception as e:
        print("ERROR:", e)
        return None
