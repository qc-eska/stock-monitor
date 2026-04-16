from datetime import datetime
import calendar

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
    "zarząd": 3,
    "decyzja": 4,
}

BLOCKLIST = [
    "notowania",
    "kurs akcji",
    "giełda",
    "podsumowanie sesji",
]


def normalize(text: str) -> str:
    return (text or "").lower()


# ----------------------------
# 📅 FILTER: ONLY CURRENT MONTH
# ----------------------------
def is_current_month():
    now = datetime.utcnow()
    return now.month, now.year


def is_recent(item: dict) -> bool:
    """
    Google News RSS nie zawsze daje daty w prostym formacie,
    więc robimy soft-filter:
    - jeśli brak daty → przepuszczamy
    - jeśli data istnieje → sprawdzamy miesiąc
    """

    pub_date = item.get("published") or item.get("date")

    if not pub_date:
        return True  # brak daty = nie blokujemy

    try:
        dt = datetime.fromisoformat(pub_date.replace("Z", ""))

        current_month, current_year = is_current_month()

        return dt.month == current_month and dt.year == current_year

    except Exception:
        return True


def score_news(text: str) -> int:
    text = normalize(text)
    score = 0

    for keyword, value in HIGH_IMPACT.items():
        if keyword in text:
            score += value

    return score


def is_relevant(text: str) -> bool:
    text = normalize(text)

    for b in BLOCKLIST:
        if b in text:
            return False

    return True


def build_alert(item: dict, score: int) -> str:
    return (
        f"📈 JSW IMPACT ALERT (score: {score})\n\n"
        f"{item.get('title')}\n\n"
        f"{item.get('url')}"
    )


def filter_news(news: list) -> list:
    alerts = []

    for item in news:
        text = f"{item.get('title','')} {item.get('url','')}"

        # 1. filtr miesiąca
        if not is_recent(item):
            continue

        # 2. blokady
        if not is_relevant(text):
            continue

        # 3. scoring
        score = score_news(text)

        if score >= 5:
            alerts.append(build_alert(item, score))

    if score >= 8:
    set_mode("red")

elif score >= 5:
    set_mode("yellow")

else:
    set_mode("green")
            
    return alerts
