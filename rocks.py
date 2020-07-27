import configparser

import rocksdb


config = configparser.ConfigParser()
config.read('config.ini')

opts = rocksdb.Options()
opts.create_if_missing = True
opts.max_open_files = int(config['rocksdb']['max_open_files'])
opts.write_buffer_size = int(config['rocksdb']['write_buffer_size'])
opts.max_write_buffer_number = int(
    config['rocksdb']['max_write_buffer_number'])
opts.target_file_size_base = int(config['rocksdb']['target_file_size_base'])

opts.table_factory = rocksdb.BlockBasedTableFactory(
    filter_policy=rocksdb.BloomFilterPolicy(
        int(config['rocksdb']['filter_policy'])),
    block_cache=rocksdb.LRUCache(2 * (1024 ** 3)),
    block_cache_compressed=rocksdb.LRUCache(500 * (1024 ** 2)))
# TODO find a way to add block_cache* in config, only this format is allowed for rocksdb


def init():
  db = rocksdb.DB(config['rocksdb']['db_file'], opts)
  return db


def createWriteBatch(items):
  batch = rocksdb.WriteBatch()
  for item in items:
    print(item.type.OperationalType)
    if item.type == "put":
      batch.put(bytes(item.key, 'utf-8'), bytes(item.value, 'utf-8'))
    elif item.type == "delete":
      batch.delete(bytes(item["key"]))
  return batch
