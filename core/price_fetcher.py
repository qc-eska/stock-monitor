import requests


URL_LIVE = "https://stooq.pl/q/l/?s=jsw_pl&i=1"
URL_DAILY = "https://stooq.pl/q/l/?s=jsw_pl"


CACHE = {
    "price": None
}


def parse(row):
    # B/D check
    if "B/D" in row:
        return None

    try:
        for v in row:
            try:
                f = float(v)
                if 5 < f < 500:
                    return f
            except:
                continue
    except:
        return None

    return None


def fetch(url):
    r = requests.get(url, timeout=10)

    if r.status_code != 200:
        return None

    lines = r.text.strip().split("\n")

    if len(lines) < 2:
        return None

    row = lines[1].split(",")

    return parse(row)


def get_jsw_price():
    price = fetch(URL_LIVE)

    if price:
        CACHE["price"] = price
        return {"price": price}

    # fallback (close price)
    price = fetch(URL_DAILY)

    if price:
        CACHE["price"] = price
        return {"price": price}

    # last known fallback
    if CACHE["price"]:
        print("USING CACHE")
        return {"price": CACHE["price"]}

    return None
