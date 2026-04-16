import requests
import time


URLS = [
    "https://stooq.pl/q/l/?s=jsw_pl&i=1",
    "https://stooq.pl/q/l/?s=jsw_pl"
]


def parse(text):
    try:
        lines = text.strip().split("\n")
        if len(lines) < 2:
            return None

        row = lines[1].split(",")

        # znajdź pierwszą sensowną cenę (Close)
        for val in row:
            try:
                v = float(val)
                if 5 < v < 500:
                    return v
            except:
                continue

        return None

    except:
        return None


def fetch(url):
    try:
        r = requests.get(url, timeout=10)

        if r.status_code == 429:
            print("RATE LIMITED - sleeping")
            time.sleep(2)
            return None

        if r.status_code != 200:
            print("HTTP ERROR:", r.status_code)
            return None

        return parse(r.text)

    except Exception as e:
        print("FETCH ERROR:", e)
        return None


def get_jsw_price():
    for url in URLS:
        price = fetch(url)

        if price:
            return {"price": price}

    print("ALL SOURCES FAILED")
    return None
