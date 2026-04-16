import requests
import xml.etree.ElementTree as ET
import re

URL = "https://news.google.com/rss/search?q=JSW+stock&hl=pl&gl=PL&ceid=PL:pl"


def clean_text(text):
    return re.sub(r"\s+", " ", text or "").strip()


def fetch_jsw_news():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

    if r.status_code != 200:
        return []

    root = ET.fromstring(r.content)

    news = []

    for item in root.findall(".//item"):
        title = item.find("title")
        link = item.find("link")

        if not title or not link:
            continue

        news.append({
            "title": clean_text(title.text),
            "url": link.text
        })

    return news
