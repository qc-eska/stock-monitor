import sqlite3
from pathlib import Path

from config import SEEN_DB_PATH


db_path = Path(SEEN_DB_PATH)
db_path.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS seen_news (
        article_id TEXT PRIMARY KEY
    )
    """
)

conn.commit()


def is_seen(article_id):
    cursor.execute("SELECT article_id FROM seen_news WHERE article_id=?", (article_id,))
    return cursor.fetchone() is not None


def mark_seen(article_id):
    cursor.execute(
        "INSERT OR IGNORE INTO seen_news(article_id) VALUES (?)",
        (article_id,),
    )
    conn.commit()
