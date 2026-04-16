import requests


def get_jsw_price():
    url = "https://stooq.pl/q/l/?s=jsw&f=sd2t2ohlcv&h&e=json"

    r = requests.get(url)
    data = r.json()

    if not data or "close" not in data["data"][0]:
        return None

    item = data["data"][0]

    return {
        "price": item["close"],
        "change": item["change"],
        "change_pct": item["changes"],
        "time": item["time"]
    }
