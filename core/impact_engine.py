import re

# Słowa kluczowe → wpływ na kurs
HIGH_IMPACT = {
    "wynik": 5,
    "zysk": 5,
    "strata": 5,
    "ebitda": 5,
    "przychody": 4,
    "prognoza": 4,
    "ostrzeżenie": 6,
    "odpis": 6,
    "restrukturyzacja": 6,
    "kopalnia": 4,
    "produkcja": 4,
    "wydobycie": 4,
    "strajk": 7,
    "protest": 6,
    "awaria": 6,
    "przerwa": 5,
    "podatki": 5,
    "ets": 5,
    "energia": 3,
    "węgiel": 3,
    "koks": 3,
    "kontrakt": 4,
    "umowa": 3,
    "analiza": 2,
    "rekomendacja": 3,
}

BLOCKLIST = [
    "kurs akcji",
    "notowania",
    "giełda dziś",
    "podsumowanie sesji",
]


def normalize(text: str):
    return (text or "").lower()


def score_news(text: str) -> int:
    text = normalize(text)
    score = 0

    for keyword, value in HIGH_IMPACT.items():
        if keyword in text:
            score += value

    return score


def is_relevant(text: str) -> bool:
    text = normalize(text)

    # blokujemy szum
    for b in BLOCKLIST:
        if b in text:
            return False

    return True


def build_alert(item: dict, score: int):
    return (
        f"📈 JSW IMPACT ALERT (score: {score})\n\n"
        f"{item.get('title')}\n\n"
        f"{item.get('url')}"
    )


def filter_news(news: list):
    alerts = []

    for item in news:
        text = item.get("title", "") + " " + item.get("url", "")

        if not is_relevant(text):
            continue

        score = score_news(text)

        # próg decyzji
        if score >= 5:
            alerts.append(build_alert(item, score))

    return alerts
