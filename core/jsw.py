def fetch_jsw_news():
    # TODO: później RSS / Bankier / Stooq / Investing
    return [
        {"title": "JSW test news", "url": "https://example.com"}
    ]


def analyze(news):
    alerts = []

    for item in news:
        alerts.append(
            f"📈 JSW ALERT\n{item['title']}\n{item['url']}"
        )

    return alerts
