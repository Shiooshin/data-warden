import rocksdb
import json
from typing import Dict
from grabby.storage.handler import StorageHandler


class RocksdbHandler(StorageHandler):
    __repository_db__ = None
    __statistics_db__ = None

    repository_db_path = "/opt/rocksdb/repository.db"
    statistics_db_path = "/opt/rocksdb/statistics.db"

    def __init__(self) -> None:
        super().__init__()
        self.__repository_db__ = \
            self.get_db_instnce(self.repository_db_path, self.db_config())

        self.__statistics_db__ = \
            self.get_db_instnce(self.statistics_db_path, self.db_config())

    def __write_batch__(self, db, data: Dict = dict()):
        batch = rocksdb.WriteBatch()

        if not data:
            return

        for key, value in data.items():
            byte_key = bytes(key, 'utf-8')
            byte_value = json.dumps(value).encode('utf-8')
            batch.put(byte_key, byte_value)

        db.write(batch)

    def __get_batch__(self, db, keys: list = list()):
        b_keys = list(map(lambda key: bytes(key, 'utf-8'), keys))
        return db.multi_get(b_keys)

    def write_repository_batch(self, data: Dict = dict()):
        self.__write_batch__(db=self.__repository_db__, data=data)

    def write_statistics_batch(self, data: Dict = dict()):
        self.__write_batch__(db=self.__statistics_db__, data=data)

    def read_repository_batch(self, keys: list = list()):
        return self.__get_batch__(self.__repository_db__, keys)

    def read_statistics_batch(self, keys: list = list()):
        return self.__get_batch__(self.__repository_db__, keys)

    def get_db_instnce(self, db_path, opts):
        return rocksdb.DB(db_path, opts)

    def db_config(self, prod: bool = False):
        opts = rocksdb.Options()

        if prod:
            opts.create_if_missing = True
            opts.max_open_files = 300000
            opts.write_buffer_size = 67108864
            opts.max_write_buffer_number = 3
            opts.target_file_size_base = 67108864

            opts.table_factory = rocksdb.BlockBasedTableFactory(
                filter_policy=rocksdb.BloomFilterPolicy(10),
                block_cache=rocksdb.LRUCache(2 * (1024 ** 3)),
                block_cache_compressed=rocksdb.LRUCache(500 * (1024 ** 2)))

        else:
            opts.create_if_missing = True
        return opts
