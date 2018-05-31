# データの整形・入手
import codecs
import random

pos_name = '../data/rt-polaritydata/rt-polarity.pos'
neg_name = '../data/rt-polaritydata/rt-polarity.neg'
smt_name = '../data/sentiment.txt'
f_encoding = "cp1252"

result = []

# ポジティブデータの読み込み
with codecs.open(pos_name, 'r', f_encoding) as f_pos:
    result.extend(['+1 {}'.format(line.strip()) for line in f_pos])

# ネガティブデータの読み込み
with codecs.open(neg_name, 'r', f_encoding) as f_neg:
    result.extend(['-1 {}'.format(line.strip()) for line in f_neg])

# シャッフル
random.shuffle(result)

# 書き出し
with codecs.open(smt_name, 'w', f_encoding) as f_out:
    print(*result, sep='\n', file=f_out)

# 数の確認
cnt_pos = 0
cnt_neg = 0
with codecs.open(smt_name, 'r', f_encoding) as f_out:
    for line in f_out:
        if line.startswith('+1'):
            cnt_pos += 1
        elif line.startswith('-1'):
            cnt_neg += 1

print('pos:{}, neg:{}'.format(cnt_pos, cnt_neg))
