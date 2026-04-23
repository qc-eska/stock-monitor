# Stock Monitor

Bot monitoruje wysokowagowe newsy o JSW i bliskim otoczeniu spolki, wysyla alerty na Telegram i zmienia branding kanalu.
Dodatkowo monitoruje kurs JSW, wysyla raport godzinowy i alert przy zmianie ceny o co najmniej zadany prog procentowy.

Domyslnie monitor korzysta z kilku zrodel:

- `JSW RSS Aktualnosci` - oficjalne aktualnosci spolki
- `JSW RSS Raporty` - oficjalne raporty biezace spolki
- `JSW Aktualnosci` - fallback HTML dla biura prasowego JSW
- `JSW Raporty` - fallback HTML dla raportow biezacych JSW
- `Bankier RSS` i `Bankier HTML` - dodatkowe zrodlo mediowe

## Wymagane zmienne srodowiskowe

- `TELEGRAM_TOKEN` - token bota Telegram
- `CHAT_ID` - docelowy chat lub kanal
- `CHECK_INTERVAL` - odstep miedzy kolejnymi cyklami w sekundach, domyslnie `300`
- `REQUEST_TIMEOUT` - timeout zapytan HTTP w sekundach, domyslnie `15`
- `SEEN_DB_PATH` - sciezka do pliku SQLite z historia wyslanych newsow
- `HOURLY_REPORT_INTERVAL` - odstep miedzy raportami kursu, domyslnie `3600`
- `PRICE_ALERT_THRESHOLD_PERCENT` - prog alertu zmiany ceny wzgledem ostatniego alertu, domyslnie `1.0`
- `MIN_NEWS_PRIORITY` - minimalna waga newsa wysylanego na Telegram, domyslnie `2`
- `PRICE_MODE_THRESHOLD_PERCENT` - prog dziennej zmiany kursu do ustawiania tytulu kanalu, domyslnie `1.0`

## Zakres wysokowagowych newsow

Bot preferuje tylko sygnaly o realnym znaczeniu dla JSW:

- `JSW` - wyniki, produkcja, kopalnie, koksownie, awarie, strajki, decyzje zarzadu
- `WEGIEL/KOKS` - ceny i zdarzenia dotyczace wegla koksowego oraz koksu
- `HUTNICTWO` - duze zdarzenia popytowe po stronie stali i hut
- `REGULACJE` - ETS, CBAM, pomoc publiczna i inne decyzje o realnym wplywie kosztowym

## Tytul kanalu Telegram

Tytul kanalu jest oparty na aktualnym kursie JSW oraz sentymencie ostatniego przepuszczonego newsa.

W godzinach sesji kurs ustawia tryb wedlug dziennej zmiany:

- zmiana >= `PRICE_MODE_THRESHOLD_PERCENT` ustawia `JSW - WZROSTY`
- zmiana <= `-PRICE_MODE_THRESHOLD_PERCENT` ustawia `JSW - SPADKI`
- mniejsza zmiana ustawia `JSW - NEUTRAL`

News, ktory przejdzie filtr wysokiej wagi, moze pozniej nadpisac tryb kanalu swoim sentymentem:

- `bullish` ustawia `JSW - WZROSTY`
- `bearish` ustawia `JSW - SPADKI`
- `neutral` ustawia `JSW - NEUTRAL`

Sentyment newsa jest liczony z tytulu na podstawie slow pozytywnych i negatywnych.

## Railway

Na Railway ustaw `SEEN_DB_PATH` na sciezke w trwalym volume, na przyklad `/data/stock-monitor.db`.
Bez volume bot moze po restarcie ponownie wyslac te same wiadomosci.

## Start

```bash
pip install -r requirements.txt
python main.py
```
