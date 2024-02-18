from typing import List, Dict
import os
import threading
import requests

import logging.config
from config import dict_config


logging.config.dictConfig(dict_config)
loger = logging.getLogger("sender")


class Sender:
    """Класс выполняющий подключение и синхронизацию файлов на Yandex disc"""

    def __init__(self, FOLDER_CLOUD, TOKEN, FOLDER):
        loger.info("Инициализация класса Sender")
        self.FOLDER_CLOUD = FOLDER_CLOUD
        self.FOLDER_LOCAL = FOLDER
        self.TOKEN = TOKEN
        self.headers = {'Authorization': f'OAuth {TOKEN}'}
        self.url_delete: str = 'https://cloud-api.yandex.net/v1/disk/resources'
        self.url_update: str = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        self.url_user_disk: str = 'https://cloud-api.yandex.net/v1/disk/'
        self.session = requests.session()

    def first_connection(self):
        """Метод выполняющий первое тестовое подключение к Yandex disc"""

        result = self.session.get(url=self.url_user_disk, headers=self.headers)
        if result.status_code == 200:
            return True
        else:
            return False

    def delete_to_yandex(self, name_file: str):
        """Метод выполняющий удаление файлов с Yandex disc"""

        params: Dict = {
            'path': self.FOLDER_CLOUD + name_file,
            'permanently': 'true'
        }
        response = self.session.delete(url=self.url_delete, headers=self.headers, params=params)

        if response.status_code == 204:
            loger.info(f'Успешно! Файл {name_file} удален из Yandex disc')
        else:
            loger.error(f'Произошла ошибка при удалении файла {name_file} файл не был удален из Yandex disc')

    def update_to_yandex(self, name_file: str):
        """Метод выполняющий добавление файлов на Yandex disc"""

        params: Dict = {
            'path': self.FOLDER_CLOUD + name_file,
            'overwrite': 'true'
        }
        response = self.session.get(url=self.url_update, headers=self.headers, params=params)

        if response.status_code == 200:
            upload_url = response.json()['href']
            filepath = os.path.join(self.FOLDER_LOCAL, name_file)
            upload_response = self.session.put(upload_url, files={'file': filepath})

            if upload_response.status_code == 201:
                loger.info(f'Успешно! Файл {name_file} записан на Yandex disc')
            else:
                loger.error(f"Произошла ошибка при записи файла {name_file} на Yandex disc")
        else:
            loger.error(f"Произошла ошибка при получении url для записи файла {name_file}")

    def run_sender(self, list_delete: List[tuple], list_add: List[tuple]):
        """Основной метод выполняющий синхронизацию файлов на Yandex disc"""

        loger.warning("Запускается основной процесс синхранизации файлов на Yandex disc")
        threads_del: List[threading.Thread] = []
        threads_upd: List[threading.Thread] = []

        if list_delete:
            loger.warning("Запускаются процессы на удаление файлов из Yandex disc")
            for file in list_delete:
                thread = threading.Thread(target=self.delete_to_yandex, args=(file[0], ))
                thread.start()
                threads_del.append(thread)
            for thread in threads_del:
                thread.join()
        else:
            loger.info("Удаление файлов на Yandex disc не требуется")

        if list_add:
            loger.warning("Запускаются процессы на добавление файлов на Yandex disc")
            for file in list_add:
                thread = threading.Thread(target=self.update_to_yandex, args=(file[0], ))
                thread.start()
                threads_upd.append(thread)
            for thread in threads_upd:
                thread.join()
        else:
            loger.info("Обновление файлов на Yandex disc не требуется")
