# KVS内の反復処理
import gzip
import json
import re
import leveldb


db_name = '../data/test_db'

# LevelDBオープン
db = leveldb.LevelDB(db_name)

# 条件入力
clue = 'Japan'.encode()
result = [value[0].decode() for value in db.RangeIter() if value[1] == clue]

# 件数表示
print('{}件'.format(len(result)))

