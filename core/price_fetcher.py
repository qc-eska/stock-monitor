import requests


STOOQ_URL = "https://stooq.pl/q/l/?s=jsw&i=1"
STOOQ_BACKUP = "https://stooq.pl/q/l/?s=jsw"


def parse_stooq(csv_text):
    try:
        lines = csv_text.strip().split("\n")

        if len(lines) < 2:
            return None

        row = lines[1].split(",")

        # Close price
        price = row[4]

        if not price or price == "0":
            return None

        return float(price)

    except Exception as e:
        print("PARSE ERROR:", e)
        return None


def fetch_from_stooq(url):
    try:
        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            print("STOOQ HTTP ERROR:", r.status_code)
            return None

        return parse_stooq(r.text)

    except Exception as e:
        print("STOOQ FETCH ERROR:", e)
        return None


def get_jsw_price():
    # PRIMARY SOURCE
    price = fetch_from_stooq(STOOQ_URL)

    if price:
        return {"price": price}

    print("Primary source failed, trying backup...")

    # BACKUP SOURCE
    price = fetch_from_stooq(STOOQ_BACKUP)

    if price:
        return {"price": price}

    print("Backup source also failed")

    return None
