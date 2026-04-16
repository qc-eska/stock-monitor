import feedparser
import re

URLS = [
    "https://www.bankier.pl/rss/wiadomosci.xml",
]


def clean_text(text):
    return re.sub(r"\s+", " ", text or "").strip()


def classify_text(text):
    text = text.lower()

    # 🎯 HIGH (bezpośrednie JSW)
    if "jsw" in text or "jastrzębska" in text:
        return "jsw"

    # 🌍 MEDIUM (sektor)
    sector_keywords = [
        "węgiel",
        "górnictwo",
        "koks",
        "energetyka",
        "spółki węglowe"
    ]

    if any(k in text for k in sector_keywords):
        return "sector"

    return None


def fetch_jsw_news(limit=10):
    all_news = []

    for url in URLS:
        print("[FETCH]", url)

        feed = feedparser.parse(url)
        print(f"[DEBUG] total entries: {len(feed.entries)}")

        for entry in feed.entries:
            title = clean_text(entry.get("title", ""))
            link = entry.get("link", "")

            if not title or not link:
                continue

            tag = classify_text(title)

            if not tag:
                continue

            print(f"[MATCH:{tag.upper()}]", title)

            all_news.append({
                "title": title,
                "url": link,
                "type": tag
            })

    # deduplikacja
    unique = {}
    for n in all_news:
        unique[n["title"]] = n

    final_news = list(unique.values())[:limit]

    print(f"[FETCHED TOTAL] {len(final_news)}")

    return final_news
