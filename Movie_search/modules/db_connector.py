import datetime
from collections import defaultdict

from dotenv import load_dotenv
import os

from typing import Any

import pymysql
import pymysql.cursors
from pymongo import MongoClient, errors, ReadPreference

# # Включил журнал (логирование)
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
# Загружаю переменные из файла .env
load_dotenv()

# сделаем защищенный клас для открытия и закрытия connection с MySQL
class _MySQLConnection:
    def __init__(self, config):
        self.config = config
        self.connection = None

    def __enter__(self):
        """ открываем connection и возвращаем его наружу """
        self.connection = pymysql.connect(**self.config)

        return self.connection          # возвращаем его наружу

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ закрываем connection """
        if self.connection:
            self.connection.close()

        return False

class DBConnector:
    """ Менеджер для работы с базой данных MySQL и mongoDB """

    # def __init__(self, host='localhost', port=3306, user='root', password='', database='it_school'):
    def __init__(self, host=os.getenv("MYSQL_HOST"), port=int(os.getenv("MYSQL_PORT")), user=os.getenv("MYSQL_USER"),
                 password=os.getenv("MYSQL_PASSWORD"), database=os.getenv("MYSQL_DATABASE"),
                 mongo_base=os.getenv("MONGO_DATABASE"), mongo_collection=os.getenv("MONGO_COLLECTION")):
        self.config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database,
            'charset': 'utf8mb4',
            'autocommit': False
        }
        self.mongo_base = mongo_base
        self.mongo_collection = mongo_collection

        self._set_connection(database)

    def _set_connection(self, database):
        """
        Проверка подключения к MySQL & MongoDB
        :param database: конфигурационный список параметров подключения к MySQL
        :return:
        """
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    if result[0] == 1:
                        print(f" Подключение к MySQL БД:'{database}' прошло успешно.")
            # MongoDB connection
            self.mongo_client = MongoClient(
                host=os.getenv("MONGO_HOST"),
                port=int(os.getenv("MONGO_PORT")),
                username=os.getenv("MONGO_USER"),
                password=os.getenv("MONGO_PASSWORD"),
                authSource=os.getenv("MONGO_DATABASE"),
                authMechanism="DEFAULT",
                ssl=False,
                read_preference=ReadPreference.PRIMARY
            )
            self.mongo_client.admin.command("ping")
            self.mongo_db = self.mongo_client[self.mongo_base]
            self.courses_collection = self.mongo_db[self.mongo_collection]
            print(f" Подключение к MongoDB БД:'{self.mongo_base}' прошло успешно.")

        except errors.ConnectionFailure:
            # print(" Ошибка подключения к MongoDB")
            print(" Ошибка подключения к MongoDB")
            raise
        except errors.OperationFailure:
            print(" Ошибка авторизации или запроса")
            raise
        except pymysql.err.OperationalError as e:
            print(f" Ошибка подключения к MySQL: {e}")
            conn = pymysql.connect(**self.config)
            raise

        except Exception as e:
            print(f" Ошибка подключения к БД: {e}")
            raise

    def get_connection(self):
        """ получаем объект connection для with """
        return _MySQLConnection(self.config)

    def check_connection(self) -> Any:

        print(" Добро пожаловать! Все подключения к базам данным проверены, приятного \"полёта\"")

    def query_execute(self, query: str, params: tuple = None, fetch: str = None) -> Any:
        """
        Выполнение SQL запроса
        :param query: SQL запрос
        :param params: параметры запроса
        :param fetch: 'one' - читаем одну запись, 'all' - все записи, None - количество строк
        :return: Query result / number of rows
        """
        with self.get_connection() as connection:
            try:
                # print(query)
                with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                    cursor.execute(query, params)
                    if fetch == 'one':
                        result = cursor.fetchone()
                    elif fetch == 'all':
                        result = cursor.fetchall()
                    else:
                        result = cursor.rowcount

                    return result

            except Exception as e:

                print(f" Ошибка выполнения SQL запроса: {e}")
                print(f" SQL запрос: {query}")
                print(f" Параметры запроса: {params}")
                #raise

    def insert_log(self, search_type: str, params: dict, row_cnt: int):
        """
        Вставляем один документ в коллекцию mongoDB
        :param search_type: тип поиска "keyword" / "genre_year"
        :param params: параметры поиска keyword" / "genre_name", "year_start", "year_stop"
        :param row_cnt: количество найденных фильмов
        :return:
        """
        log = defaultdict()
        log["timestamp"] = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        log["search_type"] = search_type
        log["params"] = params
        log["results_count"] = row_cnt

        return self.courses_collection.insert_one(log)

    def read_log(self, pipeline: list)-> list[dict]:
        """
        Выполняем агрегатный запрос в mongoDB
        :param pipeline: агрегатный запрос
        :return: список словарей
        """
        return list(self.courses_collection.aggregate(pipeline))


db_connector = DBConnector()
