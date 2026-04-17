import time

from core.jsw import fetch_jsw_news
from core.news_filter import process_news
from core.price_monitor import process_quote
from core.quote import fetch_jsw_quote
from config import CHECK_INTERVAL
from telegram.channel_branding import set_mode
from telegram.bot import send_message


def run_cycle():
    print("TICK: fetching news...")

    try:
        quote = fetch_jsw_quote()
        print("[QUOTE]", quote)
        process_quote(quote, send_message)
    except Exception as exc:
        print("[ERROR QUOTE]", exc)

    articles = fetch_jsw_news()

    print("[DEBUG] RAW ARTICLES:", articles)
    print(f"[FOUND] {len(articles)} articles")

    for article in articles:
        print("[DEBUG] ARTICLE:", article)

        result = process_news(article)

        print("[DEBUG] RESULT:", result)

        if not result:
            continue

        message = result["message"]

        print("[SEND]", message)

        send_message(message)
        set_mode(result["mode"])


def main():
    print("🚀 JSW CLEAN MONITOR STARTED")

    while True:
        try:
            run_cycle()
        except Exception as e:
            print("[ERROR MAIN LOOP]", e)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
