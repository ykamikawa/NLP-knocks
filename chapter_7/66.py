# MongoDBの検索件数の取得
import json
from pymongo import MongoClient
from bson.objectid import ObjectId


def support_ObjectId(obj):
    '''
    json.dumps()でObjectIdを処理するための関数
    ObjectIdはjsonエンコードできない型なので,文字列型に変換

    戻り値:
    ObjectIdから変換した文字列
    '''
    if isinstance(obj, ObjectId):
    # 文字列として扱う
        return str(obj)
    raise TypeError(repr(obj) + " is not JSON serializable")


# MongoDBのデータベースtestdbにコレクションartistにアクセス
client = MongoClient()
db = client.testdb
collection = db.artist

# 検索
print("活動場所がJapanの件数: ", len(list(collection.find({"area": "Japan"}))))
