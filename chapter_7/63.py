# KVSの検索
import gzip
import json
import re
import leveldb


file_name = '../data/artist.json.gz'
db_name = '../data/test_db2'

# keyをnameとidに分割するための正規表現
pattern = re.compile(
        r'''
        ^
        (.*) # name
        \t # 区切り
        (\d+) # id
        $
        ''', re.VERBOSE + re.DOTALL)

# LevelDB,ない時だけ作成
try:
    db = leveldb.LevelDB(db_name, error_if_exists=True)

    # gzファイル読み込み,パース
    with gzip.open(file_name) as f:
        for line in f:
            data_json = json.loads(line)

            # name+idとtagsをDBへ追加
            key = data_json['name'] + '\t' + str(data_json['id'])
            # tagsはない場合がある
            value = data_json.get('tags')
            if value is None:
                value = []
            db.Put(key.encode(), json.dumps(value).encode())

    print("{}件登録しました".format(len(list(db.RangeIter(include_value=False)))))
except:
    db = leveldb.LevelDB(db_name)
    print('既存のDBを使います.')

# 条件入力
clue = input('アーティスト名を入力してください--> ')
hit = False

# アーティスト名+'\t'で検索
for key, value in db.RangeIter(key_from=(clue + '\t').encode()):
    # keyをnameとidに戻す
    match = pattern.match(key.decode())
    name = match.group(1)
    id = match.group(2)
    # 異なるアーティストになったら終了
    if name != clue:
        break
    # タグ情報取得
    tags = json.loads(value.decode())
    print('{}(id:{})のタグ情報:'.format(name, id))
    if len(tags) > 0:
        for tag in tags:
            print('\t{}({})'.format(tag['value'], tag['count']))
    else:
        print('\tタグはありません')
    hit = True

if not hit:
    print('{}は登録されていません'.format(clue))

