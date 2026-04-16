import hashlib
from datetime import datetime, timedelta

# cache na duplikaty
SEEN_HASHES = set()

# słowa kluczowe (ważne)
POSITIVE = ["zysk", "rekord", "umowa", "wzrost", "kontrakt"]
NEGATIVE = ["strata", "spadek", "zadłużenie", "problemy", "cięcia", "zwolnienia"]

# must-have (bez tego odrzucamy)
REQUIRED = ["jsw", "jastrzębska"]


def is_relevant(text):
    text = text.lower()
    return any(word in text for word in REQUIRED)


def is_duplicate(text):
    h = hashlib.md5(text.encode()).hexdigest()
    if h in SEEN_HASHES:
        return True
    SEEN_HASHES.add(h)
    return False


def score_news(text):
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


def format_message(title, url, score):
    emoji = "⚖️"

    if score > 0:
        emoji = "📈"
    elif score < 0:
        emoji = "📉"

    return f"{emoji} {title}\n{url}"


def process_news(article):
    """
    article = {
        "title": "...",
        "url": "...",
        "publishedAt": "..."
    }
    """

    title = article.get("title", "")
    url = article.get("url", "")

    # 1. filtr JSW
    if not is_relevant(title):
        return None

    # 2. duplikaty
    if is_duplicate(title):
        return None

    # 3. scoring
    score = score_news(title)
    mode = classify_score(score)

    # 4. format
    message = format_message(title, url, score)

    return {
        "message": message,
        "mode": mode,
        "score": score
    }
