import re

import requests
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT


QUOTE_URL = "https://www.bankier.pl/inwestowanie/profile/quote.html?symbol=JSW"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/135.0.0.0 Safari/537.36"
    )
}


def parse_decimal(value):
    normalized = (
        value.replace("\xa0", "")
        .replace(" ", "")
        .replace("zł", "")
        .replace("%", "")
        .replace(",", ".")
        .strip()
    )
    return float(normalized)


def fetch_jsw_quote():
    response = requests.get(QUOTE_URL, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    text = soup.get_text("\n", strip=True)

    price_match = re.search(r"JSW SA\s+\(JSW\)\s+(\d+,\d+)\s*zł", text)
    change_match = re.search(r"([+-]\d+,\d+)%", text)
    time_match = re.search(
        r"((?:Pn|Wt|Śr|Czw|Pt|Sob|Niedz)\.\s+\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})",
        text,
    )

    if not price_match or not change_match:
        raise ValueError("Could not parse JSW quote from Bankier page")

    return {
        "price": parse_decimal(price_match.group(1)),
        "change_percent": parse_decimal(change_match.group(1)),
        "timestamp": time_match.group(1) if time_match else "brak godziny",
        "url": QUOTE_URL,
    }
