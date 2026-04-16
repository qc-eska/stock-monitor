import requests

URL = "https://stooq.pl/q/l/?s=jsw_pl"


def get_jsw_price():
    try:
        r = requests.get(URL, timeout=10)

        print("RAW:", r.text)

        lines = r.text.strip().split("\n")

        if len(lines) < 2:
            return None

        row = lines[1].split(",")

        # CSV format:
        # 0 symbol
        # 1 date
        # 2 time
        # 3 open
        # 4 high
        # 5 low
        # 6 close  ← TO JEST NAJPEWNIEJSZE

        close = row[6]

        price = float(close)

        return {
            "price": price,
            "currency": "PLN"
        }

    except Exception as e:
        print("ERROR:", e)
        return None
