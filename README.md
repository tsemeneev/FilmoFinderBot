# ФильмоПоиск (@FilmoFinderBot)


ФильмоПоиск - это телеграм-бот, который поможет вам найти фильмы, сериалы, аниме, мультфильмы и шоу по названию. Бот предоставляет постер, описание и ссылку для просмотра в браузере в хорошем качестве.

## Стек технологий

- Selenium (Chrome) - для автоматизации веб-браузера Chrome
- BeautifulSoup4 (bs4) - для парсинга HTML-кода страницы с результатами поиска
- Aiogram - для разработки телеграм-бота

## Установка и настройка

1. Клонируйте репозиторий:

```bash
   git clone https://github.com/tsemeneev/FilmoFinderBot.git 
   ```
2. В каталоге проекта создайте и активируйте виртуальное окружение:
```bash
    python3 -m venv venv
```
```bash
    . venv/bin/activate
```

3. Установите зависимости:
```bash
    pip install -r requirements.txt
```

4. Запустите бота:

```bash 
   python bot.py
   ```


### Использование


Добавьте бота [FilmoFinderBot](https://t.me/FilmoFinderBot) в Telegram.  
Введите название фильма, сериала, аниме, мультфильма или шоу, которое вы хотите найти.
Бот пришлет вам постер, описание и ссылку для просмотра в браузере в хорошем качестве.

### Вклад
Вы можете внести свой вклад в развитие проекта, создавая новые функции, исправляя ошибки и улучшая существующий код. Присылайте свои пул-реквесты на GitHub.


#### Автор
Проект разработан и поддерживается [@s_tee](https://t.me/s_tee)