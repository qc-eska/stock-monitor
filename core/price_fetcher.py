import requests
import json


URL = "https://query1.finance.yahoo.com/v8/finance/chart/JSW.WA"


def get_jsw_price():
    try:
        r = requests.get(URL, timeout=10)

        if r.status_code != 200:
            print("HTTP ERROR:", r.status_code)
            return None

        data = r.json()

        result = data.get("chart", {}).get("result")

        if not result:
            print("NO RESULT")
            return None

        meta = result[0].get("meta", {})

        price = meta.get("regularMarketPrice")

        if price is None:
            print("NO PRICE FIELD")
            return None

        return {
            "price": float(price)
        }

    except Exception as e:
        print("FETCH ERROR:", e)
        return None
