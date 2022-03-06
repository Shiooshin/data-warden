from typing import Dict
import rocksdb


def main():
    db = rocksdb.DB("/opt/rocksdb/test.db", db_config())
    write_batch(db, prepare_batch())


def prepare_batch():
    pass


def write_batch(db, data: Dict = dict()):
    batch = rocksdb.WriteBatch()

    if not data:
        return

    for key, value in data.items():
        byte_key = bytes(key, 'utf-8')
        byte_value = bytes(value, 'utf-8')
        batch.put(byte_key, byte_value)

    db.write(batch)


def get_batch(db, keys: Dict = list()):
    return db.multi_get(keys)


def db_config(prod: bool = False):
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


if __name__ == "__main__":
    main()
