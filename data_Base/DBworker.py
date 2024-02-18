from typing import Dict, List

from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import delete, select, and_

import logging.config
from config import dict_config

engine = create_engine('sqlite:///Cloud.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

logging.config.dictConfig(dict_config)
loger = logging.getLogger("DBworker")


class Files(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    name_file = Column(String(255), nullable=False)
    time_file = Column(Float, nullable=False)


class Methods:
    """Методы для работы с Базой данных"""

    def __init__(self):
        loger.info("Инициализация класса Methods")
        Base.metadata.create_all(engine)

    def get_files(self) -> List[tuple]:
        """Метод для получение всех доступных данных о файле из таблицы"""
        loger.info("Выполняется получение данных из базы данных")
        res = session.execute(select(Files)).all()
        return [(col[0].name_file, col[0].time_file) for col in res]

    def get_list_update_data(self, data: Dict):
        """Метод обнавляющий все записи Базы данных"""
        loger.info("Запускается синхронизация данных базы данных и локальной папки компьютера")
        list_to_delete: List[tuple] = data["Удалить"]
        list_to_insert: List[tuple] = data["Добавить"]

        if list_to_insert:
            list_data: List[dict] = [{"name_file": col[0], "time_file": col[1]} for col in list_to_insert]
            session.bulk_insert_mappings(Files, list_data)
            session.commit()

        if list_to_delete:
            for col in list_to_delete:
                smt = delete(Files).where(
                    Files.name_file == col[0],
                    and_(Files.time_file == col[1]
                         )
                )
                session.execute(smt)
                session.commit()
        loger.info("Записи в базе данных обновлены")
