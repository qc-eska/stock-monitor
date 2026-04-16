from scrapers.olx import fetch_olx
from scrapers.otomoto import fetch_otomoto
from scrapers.autoplac import fetch_autoplac
from scrapers.sprzedajemy import fetch_sprzedajemy
from core.analyzer import analyze_listings
from telegram.bot import send_alert
import time

CHAT_ID = "-1003889107367"

FIRST_RUN = True


def run():
    global FIRST_RUN

    send_alert("🚗 Stock monitor START")

    while True:
        try:
            listings = []

            listings += fetch_olx()
            listings += fetch_otomoto()
            listings += fetch_autoplac()
            listings += fetch_sprzedajemy()

            print("TOTAL:", len(listings))

            if FIRST_RUN:
                print("Bootstrap - no alerts")
                FIRST_RUN = False
            else:
                alerts = analyze_listings(listings)

                for alert in alerts:
                    send_alert(alert, CHAT_ID)

            print("Scan done")

        except Exception as e:
            print("ERROR:", e)
            send_alert(f"ERROR: {e}", CHAT_ID)

        time.sleep(1800)


if __name__ == "__main__":
    run()
