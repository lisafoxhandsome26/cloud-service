from dotenv import load_dotenv, find_dotenv
from os import getenv


if not find_dotenv():
    exit("Переменные окружения не загружены т.к. отсутствует файл .env")
else:
    load_dotenv()

FOLDER = getenv("FOLDER")
FOLDER_CLOUD = getenv("FOLDER_CLOUD")
FOLDER_LOG = getenv("FOLDER_LOG")
YANDEX_TOKEN = getenv("YANDEX_TOKEN")
PERIODIC_TIME = getenv("PERIODIC_TIME")
