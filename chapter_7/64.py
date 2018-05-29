# MongoDBの構築
import gzip
import json
import pymongo
from pymongo import MongoClient

file_name = '../data/artist.json.gz'
# バルクインサートする単位（件）
unit_bulk = 10000

# MongoDBのデータベースtestdbにコレクションartistを作成
client = MongoClient()
db = client.testdb
collection = db.artist

# gzファイル読み込み
with gzip.open(file_name, 'rt') as f:
    # 1行ずつパースしてbufに詰め込む
    buf = []
    for i, line in enumerate(f, 1):
        data_json = json.loads(line)
        buf.append(data_json)

        # unit_bulk件たまったらartistへバルクインサート
        if i % unit_bulk == 0:
            collection.insert_many(buf)
            buf = []
            print('{}件追加完了'.format(i))

    # 最後のunit_bulkに入らなかった半端分の追加
    if len(buf) > 0:
        collection.insert_many(buf)
        print('{}件追加完了'.format(i))

# インデックス作成
collection.create_index([('name', pymongo.ASCENDING)])
collection.create_index([('aliases.name', pymongo.ASCENDING)])
collection.create_index([('tags.value', pymongo.ASCENDING)])
collection.create_index([('rating.value', pymongo.ASCENDING)])
