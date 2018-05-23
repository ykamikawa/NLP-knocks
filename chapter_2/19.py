# 各行の1カラム目の文字列の出現頻度を求め，出現頻度の高い順に並べる
from itertools import groupby


file_name = '../data/hightemp.txt'

# 都道府県名の読み込み
with open(file_name) as f:
    lines = f.readlines()
keys = [line.split('\t')[0] for line in lines]

# 都道府県で集計し、(都道府県, 出現頻度)のリスト作成
# goupbyはソート済みが前提
keys.sort()
results = [(key, len(list(group))) for key, group in groupby(keys)]

# 出現頻度でソート
results.sort(key=lambda key: key[1], reverse=True)

# 結果出力
for result in results:
    print("{} count: {}".format(result[0], result[1]))
