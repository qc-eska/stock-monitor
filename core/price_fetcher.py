import requests


URL = "https://stooq.pl/q/l/?s=jsw_pl&i=1"


def get_jsw_price():
    try:
        print("FETCHING URL:", URL)

        r = requests.get(URL, timeout=10)

        print("STATUS:", r.status_code)
        print("RESPONSE:", r.text[:200])

        if r.status_code != 200:
            return None

        lines = r.text.strip().split("\n")

        print("LINES:", lines)

        if len(lines) < 2:
            return None

        row = lines[1].split(",")

        print("ROW:", row)

        price = float(row[4])

        return {"price": price}

    except Exception as e:
        print("ERROR FETCH:", e)
        return None
