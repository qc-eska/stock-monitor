import requests
import xml.etree.ElementTree as ET
import re

URLS = [
    # główny
    "https://news.google.com/rss/search?q=JSW&hl=pl&gl=PL&ceid=PL:pl",

    # fallback (więcej wyników)
    "https://news.google.com/rss/search?q=Jastrzębska+Spółka+Węglowa&hl=pl&gl=PL&ceid=PL:pl"
]


def clean_text(text):
    return re.sub(r"\s+", " ", text or "").strip()


def is_jsw_related(text):
    text = text.lower()
    return "jsw" in text or "jastrzębska" in text


def fetch_from_url(url):
    try:
        r = requests.get(
            url,
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

            if not is_jsw_related(title_text):
                continue

            news.append({
                "title": title_text,
                "url": link.text
            })

        return news

    except Exception as e:
        print("[ERROR] fetch_from_url:", e)
        return []


def fetch_jsw_news(limit=10):
    all_news = []

    for url in URLS:
        print("[FETCH]", url)

        news = fetch_from_url(url)

        if news:
            all_news.extend(news)

        if len(all_news) >= limit:
            break

    # usuń duplikaty po title
    unique = {}
    for n in all_news:
        unique[n["title"]] = n

    return list(unique.values())[:limit]
