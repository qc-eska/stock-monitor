import requests

CACHE = {
    "price": None
}


URL = "https://stooq.pl/q/l/?s=jsw_pl"


def parse_price(text):
    try:
        lines = text.strip().split("\n")
        if len(lines) < 2:
            return None

        row = lines[1].split(",")

        # Stooq format:
        # 0 symbol
        # 1 date
        # 2 time
        # 3 open
        # 4 high
        # 5 low
        # 6 close

        close = row[6]

        if close == "B/D":
            return None

        price = float(close)

        # sanity check (JSW nie może być 300+)
        if price < 1 or price > 200:
            print("INVALID PRICE FILTERED:", price)
            return None

        return price

    except Exception as e:
        print("PARSE ERROR:", e)
        return None


def get_jsw_price():
    try:
        r = requests.get(URL, timeout=10)

        print("STATUS:", r.status_code)
        print("RAW:", r.text)

        if r.status_code != 200:
            return fallback()

        price = parse_price(r.text)

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
