import feedparser
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

from config import REQUEST_TIMEOUT

RSS_SOURCES = [
    {
        "url": "https://www.bankier.pl/rss/wiadomosci.xml",
        "source": "Bankier RSS",
    },
    {
        "url": "https://www.jsw.pl/rss/aktualnosci",
        "source": "JSW RSS Aktualnosci",
    },
    {
        "url": "https://www.jsw.pl/rss/raporty-biezace",
        "source": "JSW RSS Raporty",
    },
]

HTML_SOURCES = [
    {
        "url": "https://www.bankier.pl/wiadomosci",
        "source": "Bankier HTML",
        "base_url": "https://www.bankier.pl",
        "link_prefixes": [],
    },
    {
        "url": "https://www.jsw.pl/biuro-prasowe/aktualnosci",
        "source": "JSW Aktualnosci",
        "base_url": "https://www.jsw.pl",
        "link_prefixes": ["/biuro-prasowe/aktualnosci/artykul/"],
    },
    {
        "url": "https://www.jsw.pl/relacje-inwestorskie/raporty-gieldowe/raporty-biezace/wyszukiwarka-raportow",
        "source": "JSW Raporty",
        "base_url": "https://www.jsw.pl",
        "link_prefixes": ["/relacje-inwestorskie/raporty-gieldowe/raporty-biezace/raport-biezacy/"],
    },
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


def normalize_link(link, base_url):
    return urljoin(base_url, link)


def is_allowed_link(link, prefixes):
    if not prefixes:
        return True

    return any(link.startswith(prefix) for prefix in prefixes)


# ======================
# RSS
# ======================
def fetch_from_rss(source_config):
    url = source_config["url"]
    source_name = source_config["source"]
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

        print(f"[MATCH RSS:{source_name}:{tag}]", title)

        news.append({
            "title": title,
            "url": link,
            "type": tag,
            "source": source_name,
        })

    return news


# ======================
# HTML fallback
# ======================
def fetch_from_html(source_config):
    url = source_config["url"]
    source_name = source_config["source"]
    base_url = source_config["base_url"]
    link_prefixes = source_config.get("link_prefixes", [])
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

            if not is_allowed_link(link, link_prefixes):
                continue

            tag = classify_text(title)
            if not tag:
                continue

            link = normalize_link(link, base_url)

            print(f"[MATCH HTML:{source_name}:{tag}]", title)

            news.append({
                "title": title,
                "url": link,
                "type": tag,
                "source": source_name,
            })

    except requests.RequestException as e:
        print(f"[ERROR HTML:{source_name}]", e)

    return news


# ======================
# MAIN
# ======================
def fetch_jsw_news(limit=10):
    all_news = []

    # RSS
    for source_config in RSS_SOURCES:
        all_news.extend(fetch_from_rss(source_config))

    # HTML fallback (jeśli mało danych)
    if len(all_news) < 3:
        for source_config in HTML_SOURCES:
            all_news.extend(fetch_from_html(source_config))

    # dedupe
    unique = {}
    for n in all_news:
        unique[(n["title"], n["url"])] = n

    final_news = list(unique.values())[:limit]

    print(f"[TOTAL NEWS] {len(final_news)}")

    return final_news
