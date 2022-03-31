from grabby.storage.handler import StorageHandler
from typing import Dict

import psycopg2


class PostgresqlHandler(StorageHandler):
    __stats_table__ = "repo_statistics"
    __repo_table__ = "repository"

    __repo_cols__ = ["name", "owner", "tags"]
    __stats_cols__ = ["repo_name", "agg_date", "star_count",
                      "watcher_count", "fork_count", "open_issues",
                      "contributors", "commits", "closed_issues"]

    __conn__ = None

    def __init__(self) -> None:
        super().__init__()

        self.__conn__ = self.get_connection()

    def write_repository_batch(self, data: Dict = dict()):
        self.__write_batch__(self.__repo_table__, self.__repo_cols__, data)

    def write_statistics_batch(self, data: Dict = dict()):
        for key, values in data.items():
            self.__write_batch__(self.__stats_table__, self.__stats_cols__, values)

    def read_repository_batch(self, keys: list = list()):
        result = self.__get_batch__(self.__repo_table__, "name", keys)
        print(result)

    def read_statistics_batch(self, keys: list = list()):
        result = self.__get_batch__(self.__stats_table__, "agg_date", keys)
        print(result)

    def __write_batch__(self, table, columns: list, data: dict = dict()):
        cursor = self.__conn__.cursor()
        values = self.__prepare_values__(columns, data)

        insert_query = \
            f"insert into {table} ({','.join(columns)}) values {values}"

        cursor.execute(insert_query)
        self.__conn__.commit()

    def __prepare_values__(self, columns, data: dict):
        values = []
        for vals in data.values():
            value_row = []
            for column in columns:
                if column in vals:
                    if isinstance(vals[column], int):
                        value_row.append(str(vals[column]))
                    elif isinstance(vals[column], list):
                        cleaned = str(vals[column]).replace("'", "")
                        value_row.append(f"'{cleaned}'")
                    else:
                        value_row.append(f"'{vals[column]}'")
                else:
                    print(f"should not miss any column, but misses {column} for value: {vals}")
            ret_row = f'({",".join(value_row)})'
            values.append(ret_row)

        ret_val = ",".join(values)
        return ret_val

    def __get_batch__(self, table, column="id", keys: Dict = list()):
        cursor = self.__conn__.cursor()
        select_query = \
            f"select * from {table} where {column} in (${','.join(keys)})"

        cursor.execute(select_query)

    def get_connection(self):
        return psycopg2.connect(
               host="localhost",
               database="repositories",
               user="postgres",
               password="postgres")
