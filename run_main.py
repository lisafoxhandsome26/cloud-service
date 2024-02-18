from celery import Celery
import redis

from main import Main
from data_Base import Methods
from Senders import Sender

import logging.config
from config import FOLDER, FOLDER_CLOUD, YANDEX_TOKEN, dict_config


redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

logging.config.dictConfig(dict_config)
loger = logging.getLogger("DBworker")


app = Celery(
    'run_main',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    broker_connection_retry_on_startup=True
)

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


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60, run_check_schedule.s())


@app.task
def run_check_schedule():
    run.main_worker()


if __name__ == "__main__":
    loger.info("Запуск сервиса синхронизации файлов main_worker")
    app.worker_main(['worker', '--beat'])

