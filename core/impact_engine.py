from datetime import datetime
import email.utils

from core.branding_engine import set_mode


# ----------------------------
# 🎯 IMPACT KEYWORDS
# ----------------------------
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


# ----------------------------
# 🔧 UTILS
# ----------------------------
def normalize(text: str) -> str:
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

    for b in BLOCKLIST:
        if b in text:
            return False

    return True


# ----------------------------
# 📅 HARD DATE FILTER (FIXED)
# ----------------------------
def is_recent(item: dict) -> bool:
    """
    Only last 30 days.
    No fallback = no old news leak.
    """

    pub_date = item.get("published") or item.get("date")

    if not pub_date:
        return False

    try:
        parsed_time = email.utils.parsedate_to_datetime(pub_date)

        now = datetime.utcnow()

        delta_days = (now - parsed_time.replace(tzinfo=None)).days

        return 0 <= delta_days <= 30

    except Exception:
        return False


# ----------------------------
# 📢 ALERT FORMAT
# ----------------------------
def build_alert(item: dict, score: int) -> str:
    return (
        f"📈 JSW IMPACT ALERT (score: {score})\n\n"
        f"{item.get('title')}\n\n"
        f"{item.get('url')}"
    )


# ----------------------------
# 🚀 MAIN ENGINE
# ----------------------------
def filter_news(news: list) -> list:
    alerts = []
    max_score = 0

    for item in news:
        text = f"{item.get('title','')} {item.get('url','')}"

        # 1. DATE FILTER (CRITICAL FIX)
        if not is_recent(item):
            continue

        # 2. BLOCKLIST
        if not is_relevant(text):
            continue

        # 3. SCORING
        score = score_news(text)

        if score > max_score:
            max_score = score

        # 4. ALERT THRESHOLD
        if score >= 5:
            alerts.append(build_alert(item, score))

    # ----------------------------
    # 🎛️ BRANDING (GLOBAL STATE)
    # ----------------------------
    if max_score >= 8:
        set_mode("red")

    elif max_score >= 5:
        set_mode("yellow")

    else:
        set_mode("green")

    return alerts
