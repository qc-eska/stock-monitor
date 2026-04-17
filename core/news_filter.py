import hashlib

from config import MIN_NEWS_PRIORITY
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
            "koks",
            "coke",
        ],
    },
    "steel_demand": {
        "priority": 2,
        "label": "HUTNICTWO",
        "keywords": [
            "stal",
            "steel",
            "hutnict",
            "huta",
            "wielki piec",
            "blast furnace",
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


def format_message(title, url, score, label, priority):
    emoji = "⚖️"

    if score > 0:
        emoji = "📈"
    elif score < 0:
        emoji = "📉"

    return f"{emoji} [{label} | WAGA {priority}] {title}\n{url}"


def process_news(article):
    title = article.get("title", "")
    url = article.get("url", "")
    news_type = article.get("type", "company")

    if is_duplicate(title):
        return None

    normalized_title = title.lower()
    priority = calculate_priority(normalized_title, news_type)
    if priority < MIN_NEWS_PRIORITY:
        return None

    score = score_news(title, news_type)
    label = HIGH_IMPACT_RULES.get(news_type, {}).get("label", "NEWS")
    mode = classify_score(score)
    message = format_message(title, url, score, label, priority)

    return {
        "message": message,
        "mode": mode,
        "score": score,
        "priority": priority,
    }
