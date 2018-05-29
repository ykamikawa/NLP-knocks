# KVSの構築
import gzip
import json
import leveldb


file_name = '../data/artist.json.gz'
db_name = '../data/test_db'

# LevelDBオープン,パース
db = leveldb.LevelDB(db_name)

# gzファイル読み込み,パース
with gzip.open(file_name, 'rt') as f:
    for line in f:
        data_json = json.loads(line)

        # key=name+id,value=areaとしてDBへ追加
        key = data_json['name'] + '\t' + str(data_json['id'])
        # areaはない場合がある
        value = data_json.get('area', '')
        # encodeメソッドでバイト列として保存
        db.Put(key.encode(), value.encode())

# 登録件数の確認
print('{}件登録しました.'.format(len(list(db.RangeIter(include_value=False)))))
