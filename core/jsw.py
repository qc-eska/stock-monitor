import feedparser
import re

URLS = [
    "https://www.bankier.pl/rss/wiadomosci.xml",
    "https://stooq.pl/rss/?f=1"
]


def clean_text(text):
    return re.sub(r"\s+", " ", text or "").strip()


def is_jsw_related(text):
    text = text.lower()
    return (
        "jsw" in text
        or "jastrzębska" in text
        or "spółka węglowa" in text
    )


def fetch_from_url(url):
    try:
        print("[FETCH]", url)

        feed = feedparser.parse(url)

        news = []

        for entry in feed.entries:
            title = clean_text(entry.get("title", ""))
            link = entry.get("link", "")

            if not title or not link:
                continue

            if not is_jsw_related(title):
                continue

            news.append({
                "title": title,
                "url": link
            })

        return news

    except Exception as e:
        print("[ERROR] fetch_from_url:", e)
        return []


def fetch_jsw_news(limit=10):
    all_news = []

    for url in URLS:
        news = fetch_from_url(url)

        if news:
            all_news.extend(news)

    # deduplikacja po title
    unique = {}
    for n in all_news:
        unique[n["title"]] = n

    final_news = list(unique.values())[:limit]

    print(f"[FETCHED TOTAL] {len(final_news)}")

    return final_news
