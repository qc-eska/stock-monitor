import hashlib

SEEN_HASHES = set()

POSITIVE = [
    "zysk", "rekord", "umowa", "wzrost", "kontrakt",
    "inwestycja", "finansowanie", "wsparcie", "dotacja"
]

NEGATIVE = [
    "strata", "spadek", "zadłużenie", "problemy",
    "cięcia", "zwolnienia", "kryzys", "upadłość",
    "ograniczenie", "zamknięcie"
]

# 🔥 NOWE: sektorowe interpretacje
SECTOR_POSITIVE = [
    "wsparcie", "dotacje", "rozwój", "inwestycje"
]

SECTOR_NEGATIVE = [
    "koniec węgla",
    "ograniczenie wydobycia",
    "zamknięcie kopalń",
    "transformacja energetyczna",
    "dekarbonizacja"
]


def is_duplicate(text):
    h = hashlib.md5(text.encode()).hexdigest()
    if h in SEEN_HASHES:
        return True
    SEEN_HASHES.add(h)
    return False


def score_news(text, news_type):
    text = text.lower()
    score = 0

    # standardowe
    for word in POSITIVE:
        if word in text:
            score += 1

    for word in NEGATIVE:
        if word in text:
            score -= 1

    # 🔥 sektorowe (ważne!)
    if news_type == "sector":
        for word in SECTOR_POSITIVE:
            if word in text:
                score += 1

        for word in SECTOR_NEGATIVE:
            if word in text:
                score -= 1

    return score


def classify_score(score):
    if score >= 1:
        return "bullish"
    elif score <= -1:
        return "bearish"
    return "neutral"


def format_message(title, url, score):
    emoji = "⚖️"

    if score > 0:
        emoji = "📈"
    elif score < 0:
        emoji = "📉"

    return f"{emoji} {title}\n{url}"


def process_news(article):
    title = article.get("title", "")
    url = article.get("url", "")
    news_type = article.get("type", "jsw")

    if is_duplicate(title):
        return None

    score = score_news(title, news_type)

    mode = classify_score(score)
    message = format_message(title, url, score)

    return {
        "message": message,
        "mode": mode,
        "score": score
    }
