import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
MYSQL_CREDS = {
    'host': 'localhost',
    'database': 'travel_bot',
    'user': 'klara',
    'password': os.getenv('MYSQL_PASSWORD')
}
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('history', "Вывести историю"),
)

HOTEL_COMMANDS = (
    ('lowprice', "Вывести самые дешевые отели в городе"),
    ('highprice', "Вывести самые дорогие отели в городе"),
    ('bestdeal', "Вывести отели наиболее подходящие по цене и располежению от центра"),
)

STATE_COMMANDS = (
    ('cancel', "Отменить команду"),
)

COMMANDS_DEC = (
    ('lowprice', "вывод самых дешевых отелей в городе"),
    ('highprice', "вывод самых дорогих отелей в городе"),
    ('bestdeal', "вывод отелей наиболее подходящих по цене и располежению от центра"),
    ('history', "вывод истории поиска отелей")
)

URL_HOTELS = "https://www.hotels.com/ho%d"
URL_LOC_SEARCH = "https://hotels4.p.rapidapi.com/locations/v2/search"
URL_PROPERTIES = "https://hotels4.p.rapidapi.com/properties/list"
URL_PHOTOS = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
HEADERS = {
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    "X-RapidAPI-Key": RAPID_API_KEY
}
