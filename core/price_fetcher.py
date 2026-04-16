import requests

URL = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=JSW.WA"

CACHE = {"price": None}


def get_jsw_price():
    try:
        r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

        print("STATUS:", r.status_code)

        data = r.json()

        result = data["quoteResponse"]["result"]

        if not result:
            return None

        price = result[0]["regularMarketPrice"]

        CACHE["price"] = price

        return {"price": price, "currency": "PLN"}

    except Exception as e:
        print("ERROR:", e)

        if CACHE["price"]:
            return {"price": CACHE["price"], "currency": "PLN"}

        return None
