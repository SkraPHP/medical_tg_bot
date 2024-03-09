# medical bot
Телеграм бот для получений уведомлений о медицинских таймаутах в теннисных матчах.

# Требования:
1. Python 3+ (язык программирования)
2. requests (для отправки запросов)
3. bs4 (для чтения html страницы)
4. selenium (для браузерной навигации)
5. pandas (для работы с датафреймами)
6. time (для создания пауз в программе)
7. json (для json структур)
8. Selenium WebDriver

# Инструкция по установке:
1. Установить [Python 3+ ](https://www.python.org/downloads/)
2. Установить пакеты python (pip install <package>)
3. Скачать selenium [WebDriver](https://chromedriver.chromium.org/downloads)
4. Создать папку, положить в него Medibot.py и chromedriver (exe-файл)
5. Создать бота в телеграм с помощью [botfather](https://t.me/botfather)
6. Подставить в файле Medibot.py в переменнную TOKEN = "<telegram_bot_token>" свой токен
7. Создать чат, куда будут отправляться сообщения ботом
8. Подставить в файле Medibot.py в переменнную chat_id = "<chat_id>" свой номер чата

# Запуск
1. Запустить скрипт Medibot.py
