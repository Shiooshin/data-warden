from handler import StorageHandler
from typing import Dict

import psycopg2


class PostgresqlHandler(StorageHandler):
    __conn__ = None

    def __init__(self) -> None:
        super().__init__()

        self.__conn__ = self.get_connection()

    def write_batch(self, data: Dict = dict()):
        cursor = self.__conn__.cursor()
        # Executing a SQL query to insert data into  table
        insert_query = ""
        cursor.execute(insert_query)
        self.__conn__.commit()

    def get_batch(self, keys: Dict = list()):
        pass

    def get_connection(self):
        return psycopg2.connect(
               host="localhost",
               database="suppliers",
               user="postgres",
               password="Abcd1234")
