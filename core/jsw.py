import feedparser
import requests
from bs4 import BeautifulSoup
import re

URLS_RSS = [
    "https://www.bankier.pl/rss/wiadomosci.xml",
]

URLS_HTML = [
    "https://www.bankier.pl/wiadomosci",
]


def clean_text(text):
    return re.sub(r"\s+", " ", text or "").strip()


def classify_text(text):
    text = text.lower()

    if "jsw" in text or "jastrzębsk" in text:
        return "jsw"

    sector_keywords = [
        "węgl", "górn", "koks", "energet", "kopaln"
    ]

    if any(k in text for k in sector_keywords):
        return "sector"

    return None


# ======================
# RSS
# ======================
def fetch_from_rss(url):
    print("[RSS]", url)

    feed = feedparser.parse(url)
    news = []

    for entry in feed.entries:
        title = clean_text(entry.get("title", ""))
        link = entry.get("link", "")

        if not title or not link:
            continue

        tag = classify_text(title)
        if not tag:
            continue

        print(f"[MATCH RSS:{tag}]", title)

        news.append({
            "title": title,
            "url": link,
            "type": tag
        })

    return news


# ======================
# HTML fallback
# ======================
def fetch_from_html(url):
    print("[HTML]", url)

    news = []

    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

        soup = BeautifulSoup(r.text, "html.parser")

        articles = soup.find_all("a")

        for a in articles:
            title = clean_text(a.text)
            link = a.get("href")

            if not title or not link:
                continue

            if len(title) < 20:
                continue

            tag = classify_text(title)
            if not tag:
                continue

            if not link.startswith("http"):
                link = "https://www.bankier.pl" + link

            print(f"[MATCH HTML:{tag}]", title)

            news.append({
                "title": title,
                "url": link,
                "type": tag
            })

    except Exception as e:
        print("[ERROR HTML]", e)

    return news


# ======================
# MAIN
# ======================
def fetch_jsw_news(limit=10):
    all_news = []

    # RSS
    for url in URLS_RSS:
        all_news.extend(fetch_from_rss(url))

    # HTML fallback (jeśli mało danych)
    if len(all_news) < 3:
        for url in URLS_HTML:
            all_news.extend(fetch_from_html(url))

    # dedupe
    unique = {}
    for n in all_news:
        unique[n["title"]] = n

    final_news = list(unique.values())[:limit]

    print(f"[TOTAL NEWS] {len(final_news)}")

    return final_news
