from telegram.channel_branding import set_mode

def filter_news(news):
    alerts = []
    max_score = 0

    for item in news:
        text = f"{item.get('title','')} {item.get('url','')}"

        # tu zakładamy że masz score_news + is_recent itd
        score = score_news(text)

        if score > max_score:
            max_score = score

        if score >= 5:
            alerts.append(
                f"📈 JSW ALERT (score: {score})\n\n"
                f"{item.get('title')}\n"
                f"{item.get('url')}"
            )

    # mode logic
    if max_score >= 8:
        set_mode("red")
    elif max_score >= 5:
        set_mode("yellow")
    else:
        set_mode("green")

    return alerts, "ok"
