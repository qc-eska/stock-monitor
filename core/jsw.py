import requests
import xml.etree.ElementTree as ET
import re

URL = "https://news.google.com/rss/search?q=JSW+OR+Jastrzębska+Spółka+Węglowa&hl=pl&gl=PL&ceid=PL:pl"


def clean_text(text):
    return re.sub(r"\s+", " ", text or "").strip()


def is_jsw_related(text):
    text = text.lower()
    return "jsw" in text or "jastrzębska" in text


def fetch_jsw_news(limit=10):
    try:
        r = requests.get(
            URL,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )

        if r.status_code != 200:
            print("[ERROR] fetch failed:", r.status_code)
            return []

        root = ET.fromstring(r.content)

        news = []

        for item in root.findall(".//item"):
            title = item.find("title")
            link = item.find("link")

            if not title or not link:
                continue

            title_text = clean_text(title.text)

            # 🔥 filtr JSW już na wejściu
            if not is_jsw_related(title_text):
                continue

            news.append({
                "title": title_text,
                "url": link.text
            })

            if len(news) >= limit:
                break

        return news

    except Exception as e:
        print("[ERROR] fetch_jsw_news:", e)
        return []
