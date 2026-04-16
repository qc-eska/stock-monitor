import requests
import re


URL = "https://finance.yahoo.com/quote/JSW.WA"


def extract_price(html):
    # szukamy patternu ceny w HTML (meta / JSON embedded)
    match = re.search(r'"regularMarketPrice":\{"raw":([0-9.]+)', html)

    if match:
        return float(match.group(1))

    # fallback regex (czasem w HTML)
    match = re.search(r'price.*?([0-9]{1,4}\.[0-9]{2})', html)

    if match:
        return float(match.group(1))

    return None


def get_jsw_price():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(URL, headers=headers, timeout=10)

        print("HTTP:", r.status_code)

        if r.status_code != 200:
            return None

        price = extract_price(r.text)

        if price:
            return {"price": price}

        print("PRICE NOT FOUND IN HTML")

        return None

    except Exception as e:
        print("FETCH ERROR:", e)
        return None
