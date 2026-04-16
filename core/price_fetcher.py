import requests

URL = "https://stooq.pl/q/l/?s=jsw_pl"


CACHE = {
    "price": None
}


def parse(text):
    lines = text.strip().split("\n")

    if len(lines) < 2:
        return None

    row = lines[1].split(",")

    # ostatnia kolumna = Close (najpewniejsze)
    try:
        price = float(row[4])
        return price
    except:
        return None


def get_jsw_price():
    try:
        r = requests.get(URL, timeout=10)

        print("STATUS:", r.status_code)
        print("RAW:", r.text)

        if r.status_code != 200:
            return None

        price = parse(r.text)

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
