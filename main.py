from typing import List, Dict, Set
import os

import logging.config
from config import dict_config


logging.config.dictConfig(dict_config)
loger = logging.getLogger("main")


class Main:
    """Основной класс для синхронизации файлов"""

    def __init__(self, FOLDER, sender, db):
        loger.info(f"Инициализация класса Main")
        self.FOLDER = FOLDER
        self.sender = sender
        self.db = db

    def changes_files(self, files_from_db: List[tuple]) -> Dict:
        """Метод проверки файлов на соответствие c базой данных"""

        loger.info("Запуск метода проверки файлов")
        files_db: Set[tuple] = set(i for i in files_from_db)
        files_local: Set[tuple] = set()

        try:
            for name_file in os.listdir(self.FOLDER):
                filepath = os.path.join(self.FOLDER, name_file)
                if os.path.isfile(filepath):
                    time_file = os.stat(filepath).st_mtime
                    files_local.add((name_file, time_file))
        except FileNotFoundError:

            loger.error("Ошибка FileNotFoundError Системе не удается найти указаный путь")
            exit("Указаня локальная папка не существует проверьте название или укажите другую")

        return {"Удалить": list(files_db.difference(files_local)), "Добавить": list(files_local.difference(files_db))}

    def main_worker(self) -> None:
        """Метод выполняющий синхронизацию файлов"""

        result: bool = self.sender.first_connection()

        if result:
            loger.info("Первое тестовое подключение прошло удачно запускается синхронизация файлов")

            list_files: List[tuple] = self.db.get_files()
            result: Dict = self.changes_files(list_files)
            self.db.get_list_update_data(result)
            self.sender.run_sender(list_delete=result["Удалить"], list_add=result["Добавить"])

            loger.info("Синхронизация файлов выполнена успешно")
        else:
            loger.error("Ошибка подключения, проверьте Интернет соединение или ТОКЕН Yandex disc")
            loger.info("Синхронизация файлов прошла с ошибкой")
