import configparser

import rocksdb


config = configparser.ConfigParser()
config.read('config.ini')


class StaticPrefix(rocksdb.interfaces.SliceTransform):
    prefix_length = int(config['rocksdb']['prefix_length'])
    def name(self):
        return b'static'

    def transform(self, src):
        return (0, self.prefix_length)

    def in_domain(self, src):
        return len(src) >= self.prefix_length

    def in_range(self, dst):
        return len(dst) == self.prefix_length


def init():
    opts = rocksdb.Options()
    opts.create_if_missing = True
    opts.max_open_files = int(config['rocksdb']['max_open_files'])
    opts.write_buffer_size = int(config['rocksdb']['write_buffer_size'])
    opts.max_write_buffer_number = int(
        config['rocksdb']['max_write_buffer_number'])
    opts.target_file_size_base = int(
        config['rocksdb']['target_file_size_base'])

    opts.table_factory = rocksdb.BlockBasedTableFactory(
        filter_policy=rocksdb.BloomFilterPolicy(
            int(config['rocksdb']['filter_policy'])),
        block_cache=rocksdb.LRUCache(2 * (1024 ** 3)),
        block_cache_compressed=rocksdb.LRUCache(500 * (1024 ** 2)))
    # TODO find a way to add block_cache* in config, only this format is allowed for rocksdb

    # https://python-rocksdb.readthedocs.io/en/latest/tutorial/#prefixextractor
    opts.prefix_extractor = StaticPrefix()

    db = rocksdb.DB(config['rocksdb']['db_file'], opts)
    return db


def create_write_batch(items):
    batch = rocksdb.WriteBatch()
    for item in items:
        if item.type.name == "put":
            batch.put(bytes(item.key, 'utf-8'), bytes(item.value, 'utf-8'))
        elif item.type.name == "delete":
            batch.delete(bytes(item.key, 'utf-8'))
    return batch
