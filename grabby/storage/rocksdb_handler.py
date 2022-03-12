import rocksdb
from typing import Dict
from handler import StorageHandler


class RocksdbHandler(StorageHandler):
    __db__ = None

    def __init__(self) -> None:
        super().__init__()
        self.__db__ = self.get_db_instnce()

    def write_batch(self, data: Dict = dict()):
        batch = rocksdb.WriteBatch()

        if not data:
            return

        for key, value in data.items():
            byte_key = bytes(key, 'utf-8')
            byte_value = bytes(value, 'utf-8')
            batch.put(byte_key, byte_value)

        self.__db__.write(batch)

    def get_batch(self, keys: Dict = list()):
        return self.__db__.multi_get(keys)

    def get_db_instnce(self):
        return rocksdb.DB("/opt/rocksdb/test.db", self.db_config())

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
