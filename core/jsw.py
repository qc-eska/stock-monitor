import feedparser
import requests
from bs4 import BeautifulSoup
import re

from config import REQUEST_TIMEOUT

URLS_RSS = [
    "https://www.bankier.pl/rss/wiadomosci.xml",
]

URLS_HTML = [
    "https://www.bankier.pl/wiadomosci",
]


def clean_text(text):
    return re.sub(r"\s+", " ", text or "").strip()


COMPANY_KEYWORDS = [
    "jsw",
    "jastrzębska spółka węglowa",
    "jastrzebska spolka weglowa",
    "bogdanka",
    "kopalnia",
    "kopalni",
    "koksownia",
    "koksownie",
    "wydobycie",
    "produkcja",
    "sprzedaż",
    "sprzedaz",
    "ebitda",
    "wyniki",
    "dywidenda",
    "zarząd",
    "zarzad",
    "związk",
    "zwiazk",
    "strajk",
    "przestój",
    "przestoj",
    "awaria",
    "pożar",
    "pozar",
    "wypadek",
]

COAL_COKE_KEYWORDS = [
    "węgiel koksowy",
    "wegiel koksowy",
    "hard coking coal",
    "coking coal",
    "koks",
    "coke",
]

STEEL_KEYWORDS = [
    "stal",
    "steel",
    "hutnict",
    "huta",
    "wielki piec",
    "blast furnace",
    "arcelormittal",
    "thyssenkrupp",
    "liberty steel",
]

REGULATION_KEYWORDS = [
    "ets",
    "eu ets",
    "cbam",
    "darmowe uprawnienia",
    "uprawnienia do emisji",
    "emisji co2",
    "pomoc publiczna",
    "komisja europejska",
    "unia europejska",
    "bruksela",
]


def contains_any(text, keywords):
    return any(keyword in text for keyword in keywords)


def classify_text(text):
    normalized = text.lower()

    if contains_any(normalized, COMPANY_KEYWORDS):
        return "company"

    if contains_any(normalized, COAL_COKE_KEYWORDS):
        return "coal_coke"

    if contains_any(normalized, REGULATION_KEYWORDS) and (
        contains_any(normalized, COAL_COKE_KEYWORDS)
        or contains_any(normalized, STEEL_KEYWORDS)
        or "jsw" in normalized
        or "jastrzębsk" in normalized
        or "jastrzebsk" in normalized
    ):
        return "regulation"

    if contains_any(normalized, STEEL_KEYWORDS):
        return "steel_demand"

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
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()

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

    except requests.RequestException as e:
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
