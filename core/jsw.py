import requests
import xml.etree.ElementTree as ET
import re

QUERY = "JSW"

RSS_URL = f"https://news.google.com/rss/search?q={QUERY}+stock&hl=pl&gl=PL&ceid=PL:pl"


def clean_text(text):
    return re.sub(r"\s+", " ", text or "").strip()


def fetch_jsw_news():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(RSS_URL, headers=headers, timeout=10)

    if r.status_code != 200:
        print("RSS ERROR:", r.status_code)
        return []

    root = ET.fromstring(r.content)

    news = []

    for item in root.findall(".//item"):
        title = item.find("title")
        link = item.find("link")

        if title is None or link is None:
            continue

        title_text = clean_text(title.text)
        link_text = link.text

        # filtr minimalny (żeby nie brać śmieci)
        if not title_text:
            continue

        news.append({
            "title": title_text,
            "url": link_text
        })

    return news
