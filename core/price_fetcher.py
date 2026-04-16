import requests


URL = "https://stooq.pl/q/l/?s=jsw_pl&i=1"


def get_jsw_price():
    try:
        r = requests.get(URL, timeout=10)

        if r.status_code != 200:
            print("HTTP ERROR:", r.status_code)
            return None

        text = r.text.strip()

        print("RAW:", text)  # debug — zobaczymy co zwraca

        lines = text.split("\n")

        if len(lines) < 2:
            print("CSV FORMAT ERROR")
            return None

        row = lines[1].split(",")

        if len(row) < 5:
            print("CSV COLUMN ERROR")
            return None

        price = float(row[4])

        return {
            "price": price
        }

    except Exception as e:
        print("FETCH ERROR:", e)
        return None
