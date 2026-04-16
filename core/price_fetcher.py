import requests
import json
import re

CACHE = {"price": None}

URL = "https://finance.yahoo.com/quote/JSW.WA"


def extract_price(html):
    try:
        # znajdź JSON root App
        match = re.search(r'root\.App\.main = (.*?);\n', html)

        if not match:
            return None

        data = json.loads(match.group(1))

        price = (
            data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]
            ["price"]["regularMarketPrice"]["raw"]
        )

        return float(price)

    except Exception as e:
        print("PARSE ERROR:", e)
        return None


def get_jsw_price():
    try:
        r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

        print("STATUS:", r.status_code)

        if r.status_code != 200:
            return None

        price = extract_price(r.text)

        if price:
            CACHE["price"] = price
            return {"price": price, "currency": "PLN"}

        if CACHE["price"]:
            print("USING CACHE")
            return {"price": CACHE["price"], "currency": "PLN"}

        return None

    except Exception as e:
        print("ERROR:", e)
        return None
