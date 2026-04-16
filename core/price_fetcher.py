import requests


def get_jsw_price():
    url = "https://stooq.pl/q/l/?s=jsw&f=sd2t2ohlcv&h&e=json"

    try:
        r = requests.get(url, timeout=10)
        data = r.json()

        item = data["data"][0]

        return {
            "price": float(item.get("close")),
            "change": item.get("change"),
            "change_pct": item.get("changes"),
            "time": item.get("time"),
        }

    except Exception as e:
        print("Price fetch error:", e)
        return None
