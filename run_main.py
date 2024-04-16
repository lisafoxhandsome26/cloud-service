from time import sleep
from main import Main
from data_Base import Methods
from Senders import Sender

import logging.config
from config import FOLDER, FOLDER_CLOUD, YANDEX_TOKEN, dict_config, PERIODIC_TIME


logging.config.dictConfig(dict_config)
loger = logging.getLogger("DBworker")


db = Methods()

sender = Sender(
    FOLDER_CLOUD=FOLDER_CLOUD,
    TOKEN=YANDEX_TOKEN,
    FOLDER=FOLDER
)

run = Main(
    FOLDER=FOLDER,
    db=db,
    sender=sender
)

if __name__ == "__main__":
    while True:
        loger.info("Запуск сервиса синхронизации файлов main_worker")
        run.main_worker()
        sleep(int(PERIODIC_TIME))
