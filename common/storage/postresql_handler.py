from datetime import date
from common.storage.handler import StorageHandler
from common.config import Config

import psycopg2


class PostgresqlHandler(StorageHandler):
    __config__ = Config()

    __stats_table__ = __config__.get('stats_table', 'postgresql')
    __repo_table__ = __config__.get('repo_table', 'postgresql')
    __etl_table__ = __config__.get('etl_table', 'postgresql')

    __repo_cols__ = ["name", "owner", "tags"]
    __stats_cols__ = ["repo_name", "agg_date", "star_count",
                      "watcher_count", "fork_count", "open_issues",
                      "contributors", "commits", "closed_issues"]
    __etl_cols__ = ["agg_date", "status"]

    __conn__ = None

    def __init__(self) -> None:
        super().__init__()

        self.__conn__ = self.get_connection()

    def write_repository_batch(self, data: dict):
        repo_names = list(map(data['name']))
        result_rows = self.read_repository_batch(repo_names)

        if len(result_rows) == len(repo_names):
            return  # nothing to do

        filtered_data = self.prepare_write_batch(repo_names, result_rows, data)

        self.__write_batch__(self.__repo_table__, self.__repo_cols__, filtered_data)

    def prepare_write_batch(self, repo_names: list, result_rows, data):
        existing_names = []
        for row in result_rows:
            existing_names.append(row['name'])

        resulting_data = {}
        for repo in repo_names:
            if repo not in existing_names:
                resulting_data[repo] = data[repo]

        return resulting_data

    def write_statistics_batch(self, data: dict):
        for key, values in data.items():
            self.__write_batch__(self.__stats_table__, self.__stats_cols__, values)

    def write_etl_batch(self, data: dict):
        self.__write_batch__(self.__etl_table__, self.__etl_cols__, data)

    def read_repository_batch(self, keys: list):
        result = self.__get_batch__(self.__repo_table__, keys, "name")
        print(result)

    def read_statistics_batch(self, keys: list):
        result = self.__get_batch__(self.__stats_table__, keys, "agg_date")
        print(result)

    def __write_batch__(self, table, columns: list, data: dict):
        cursor = self.__conn__.cursor()
        values = self.__prepare_values__(columns, data)

        insert_query = \
            f"insert into {table} ({','.join(columns)}) values {values}"

        cursor.execute(insert_query)
        self.__conn__.commit()

    def __prepare_values__(self, columns, data: dict):
        values = []
        for vals in data.values():
            values.append(self.__prepare_row__(columns, vals))

        ret_val = ",".join(values)
        return ret_val

    def __prepare_row__(self, columns, vals):
        value_row = []
        for column in columns:
            if column in vals:
                value_row.append(self.__prepare_column__(vals[column]))
            else:
                print(f"should not miss any column, but misses {column} for value: {vals}")
        return f'({",".join(value_row)})'

    def __prepare_column__(self, value):
        if isinstance(value, int):
            return str(value)
        elif isinstance(value, list):
            cleaned = str(value).replace("'", "")
            return f"'{cleaned}'"
        else:
            return f"'{value}'"

    def has_today_etl(self):
        today_str = date.today().strftime("%Y-%m-%d")
        cursor = self.__conn__.cursor()
        cursor.execute(f"select * from {self.__etl_table__} where agg_date = '{today_str}'")
        result = cursor.fetchone()

        return result is not None

    def __get_batch__(self, table, keys: list, column="id"):
        cursor = self.__conn__.cursor()
        select_query = \
            f"select * from '{table}' where {column} in (${','.join(keys)})"

        cursor.execute(select_query)  # TODO return proper result
        return cursor.fetchall()

    def get_connection(self):
        con_conf = self.__config__.get('connection', 'postgresql')
        return psycopg2.connect(
               host=con_conf['host'],
               database=con_conf['database'],
               user=con_conf['username'],
               password=con_conf['password'])

    def connection_established(self):
        if self.__conn__.closed == 0:
            return True

        return False
