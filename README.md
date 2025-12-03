# Quotes Scraper

Скрипт для автоматизации работы с сайтом [https://quotes.toscrape.com](https://quotes.toscrape.com):

- Авторизация по данным из `config.json`
- Случайный обход страниц с цитатами (через Selenium)
- Сбор данных (текст цитаты, автор, теги) и сохранение в JSON
- Поиск цитат по имени автора через CLI (`--author`)
- Переопределение количество страниц для парсинга (`--page N`)
- Логирование и retry для сетевых ошибок
- Результат работы скрипта храниться в ./qoutes/files

---

## Зависимости

- Python 3.12+
- Google Chrome / Chromium
- ChromeDriver, совместимый с версией браузера
- Библиотеки Python:
  - `selenium`
  - (опционально) `fake-useragent` — если используешь рандомный user-agent
  - любые другие пакеты, указанные в `requirements.txt`

### Установка окружения и зависимостей

```bash
python -m venv venv
source venv/bin/activate           # Windows: venv\Scripts\activate

pip install -r requirements.txt
