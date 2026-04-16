import time
import threading

from core.analyzer import analyze_listings
from core.hourly_report import send_hourly_jsw_update
from telegram.bot import send_message

from scrapers.olx import fetch_olx
from scrapers.otomoto import fetch_otomoto
from scrapers.autoplac import fetch_autoplac
from scrapers.sprzedajemy import fetch_sprzedajemy


FIRST_RUN = True


def hourly_loop():
    while True:
        try:
            send_hourly_jsw_update()
        except Exception as e:
            print("Hourly error:", e)

        time.sleep(3600)


def run():
    global FIRST_RUN

    send_message("🚀 JSW monitor LIVE (±1% alerts)")

    while True:
        try:
            listings = []

            listings += fetch_olx()
            listings += fetch_otomoto()
            listings += fetch_autoplac()
            listings += fetch_sprzedajemy()

            print("TOTAL:", len(listings))

            if FIRST_RUN:
                FIRST_RUN = False
            else:
                alerts = analyze_listings(listings)

                for alert in alerts:
                    send_message(alert)

            print("Scan done:", len(listings))

        except Exception as e:
            print("ERROR:", e)
            send_message(f"⚠️ ERROR: {e}")

        time.sleep(1800)


if __name__ == "__main__":
    threading.Thread(target=hourly_loop, daemon=True).start()
    run()
