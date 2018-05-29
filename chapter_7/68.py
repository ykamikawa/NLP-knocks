# MongoDBのソート
import json
import pymongo
from pymongo import MongoClient


# MongoDBのデータベースtestdbにコレクションartistにアクセス
client = MongoClient()
db = client.testdb
collection = db.artist

# tags.valueがdanceのオブジェクトを検索
results = collection.find({'tags.value': 'dance'})

# resultsをrating.countの値を元に照準でソート
results.sort('rating.count', pymongo.DESCENDING)

# 上位10件表示
for i, doc in enumerate(results[0:10], start=1):
    if 'rating' in doc:
        rating = doc['rating']['count']
    else:
    # ratingがないドキュメントもあるので
        rating = '(none)'
    print('{}(id:{})\t{}'.format(doc['name'], doc['id'], rating))
