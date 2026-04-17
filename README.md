# Stock Monitor

Bot monitoruje newsy o JSW i wybranych wiadomosciach sektorowych, wysyla alerty na Telegram i zmienia branding kanalu.

## Wymagane zmienne srodowiskowe

- `TELEGRAM_TOKEN` - token bota Telegram
- `CHAT_ID` - docelowy chat lub kanal
- `CHECK_INTERVAL` - odstep miedzy kolejnymi cyklami w sekundach, domyslnie `300`
- `REQUEST_TIMEOUT` - timeout zapytan HTTP w sekundach, domyslnie `15`
- `SEEN_DB_PATH` - sciezka do pliku SQLite z historia wyslanych newsow

## Railway

Na Railway ustaw `SEEN_DB_PATH` na sciezke w trwalym volume, na przyklad `/data/stock-monitor.db`.
Bez volume bot moze po restarcie ponownie wyslac te same wiadomosci.

## Start

```bash
pip install -r requirements.txt
python main.py
```
