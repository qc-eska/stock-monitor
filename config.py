import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "300"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "15"))
SEEN_DB_PATH = os.getenv("SEEN_DB_PATH", "stock-monitor.db")
