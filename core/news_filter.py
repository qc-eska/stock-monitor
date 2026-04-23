import hashlib
from datetime import datetime, timezone

from config import MAX_NEWS_AGE_HOURS, MIN_NEWS_PRIORITY
from database.db import is_seen, mark_seen

POSITIVE = [
    "zysk",
    "rekord",
    "umowa",
    "wzrost",
    "kontrakt",
    "inwestycja",
    "finansowanie",
    "wsparcie",
    "dotacja",
    "odblokowanie",
    "uruchomi",
    "wznowi",
    "increase",
    "growth",
    "rebound",
    "higher",
    "shortage",
    "disruption",
]

NEGATIVE = [
    "strata",
    "spadek",
    "zadłużenie",
    "problemy",
    "cięcia",
    "zwolnienia",
    "kryzys",
    "upadłość",
    "ograniczenie",
    "zamknięcie",
    "przestój",
    "przestoj",
    "awaria",
    "pożar",
    "pozar",
    "wypadek",
    "strajk",
    "decrease",
    "decline",
    "lower",
    "weak",
    "slowdown",
    "fall",
    "drop",
]

HIGH_IMPACT_RULES = {
    "company": {
        "priority": 3,
        "label": "JSW",
        "keywords": [
            "jsw",
            "jastrzębska spółka węglowa",
            "jastrzebska spolka weglowa",
        ],
    },
    "coal_coke": {
        "priority": 2,
        "label": "WEGIEL/KOKS",
        "keywords": [
            "węgiel koksowy",
            "wegiel koksowy",
            "hard coking coal",
            "coking coal",
            "metallurgical coal",
            "met coal",
            "premium hard coking coal",
            "fob australia",
            "coal export",
            "coal exports",
            "coal supply",
            "coal disruption",
            "coal shortage",
            "queensland coal",
            "australian coal",
            "koks",
            "coke",
            "coke price",
            "coke prices",
            "hcc coal",
            "hcc price",
            "hcc prices",
        ],
    },
    "steel_demand": {
        "priority": 2,
        "label": "HUTNICTWO",
        "keywords": [
            "crude steel production",
            "crude steel",
            "steel production",
            "steel demand",
            "steel output",
            "steel outlook",
            "short range outlook",
            "wielki piec",
            "wielkie piece",
            "blast furnace",
            "blast furnaces",
            "arcelormittal",
            "thyssenkrupp",
            "liberty steel",
        ],
    },
    "regulation": {
        "priority": 3,
        "label": "REGULACJE",
        "keywords": [
            "ets",
            "eu ets",
            "cbam",
            "darmowe uprawnienia",
            "uprawnienia do emisji",
            "pomoc publiczna",
            "komisja europejska",
            "unia europejska",
        ],
    },
}


def is_duplicate(text):
    h = hashlib.md5(text.encode()).hexdigest()

    if is_seen(h):
        return True

    mark_seen(h)
    return False


def contains_any(text, keywords):
    return any(word in text for word in keywords)


def calculate_priority(text, news_type):
    rule = HIGH_IMPACT_RULES.get(news_type)
    if not rule:
        return 0

    priority = rule["priority"]
    if contains_any(text, rule["keywords"]):
        priority += 1

    if contains_any(text, NEGATIVE) or contains_any(text, POSITIVE):
        priority += 1

    return min(priority, 4)


def parse_published_at(value):
    if not value:
        return None

    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def news_age_hours(published_at):
    if not published_at:
        return None

    now = datetime.now(timezone.utc)
    return max((now - published_at).total_seconds() / 3600, 0)


def is_too_old(published_at):
    age_hours = news_age_hours(published_at)
    if age_hours is None:
        return False

    return age_hours > MAX_NEWS_AGE_HOURS


def format_age(published_at):
    age_hours = news_age_hours(published_at)
    if age_hours is None:
        return "nieznany"

    if age_hours < 1:
        return f"{int(age_hours * 60)} min"

    if age_hours < 48:
        return f"{age_hours:.1f} h"

    return f"{age_hours / 24:.1f} dni"


def score_news(text, news_type):
    text = text.lower()
    score = 0

    for word in POSITIVE:
        if word in text:
            score += 1

    for word in NEGATIVE:
        if word in text:
            score -= 1

    return score


def classify_score(score):
    if score >= 1:
        return "bullish"
    elif score <= -1:
        return "bearish"
    return "neutral"


def format_message(title, url, score, label, priority, source, published_at):
    emoji = "⚖️"

    if score > 0:
        emoji = "📈"
    elif score < 0:
        emoji = "📉"

    age = format_age(published_at)
    published_line = (
        f"Opublikowano: {published_at.isoformat()}\n" if published_at else ""
    )

    return (
        f"{emoji} [{label} | WAGA {priority}] {title}\n"
        f"Zrodlo: {source}\n"
        f"Wiek info: {age}\n"
        f"{published_line}"
        f"{url}"
    )


def process_news(article):
    title = article.get("title", "")
    url = article.get("url", "")
    news_type = article.get("type", "company")
    source = article.get("source", "Nieznane")
    published_at = parse_published_at(article.get("published_at"))

    if is_too_old(published_at):
        print(f"[SKIP OLD NEWS] {title} age={format_age(published_at)}")
        return None

    if is_duplicate(title):
        return None

    normalized_title = title.lower()
    priority = calculate_priority(normalized_title, news_type)
    if priority < MIN_NEWS_PRIORITY:
        return None

    score = score_news(title, news_type)
    label = HIGH_IMPACT_RULES.get(news_type, {}).get("label", "NEWS")
    mode = classify_score(score)
    message = format_message(title, url, score, label, priority, source, published_at)

    return {
        "message": message,
        "mode": mode,
        "score": score,
        "priority": priority,
    }
