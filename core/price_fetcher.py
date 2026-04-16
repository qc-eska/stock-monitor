import requests


URL = "https://stooq.pl/q/l/?s=jsw&i=d"


def get_jsw_price():
    try:
        r = requests.get(URL, timeout=10)

        if r.status_code != 200:
            print("ERROR: bad response from stooq")
            return None

        text = r.text.strip()

        if not text:
            print("ERROR: empty response")
            return None

        lines = text.split("\n")

        if len(lines) < 2:
            print("ERROR: unexpected CSV format")
            return None

        data = lines[1].split(",")

        price = float(data[4])

        return {
            "price": price
        }

    except Exception as e:
        print("PRICE FETCH ERROR:", e)
        return None
