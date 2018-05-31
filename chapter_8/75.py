# 素性の重み
import codecs
import numpy as np


feature_name = '../data/feature.txt'
param_name = '../data/param.npy'
f_encoding = 'cp1252'

# 素性の読み込み
with codecs.open(feature_name, 'r', f_encoding) as f:
    features = list(f)

# 学習結果の読み込み
param = np.load(param_name)

# 重みでソートしてインデックス配列を作成
index_sorted = np.argsort(param)

# 上位,下位10件表示
print('top 10')
for index in index_sorted[:-11:-1]:
    print('\t{}\t{}'.format(param[index], features[index-1].strip() if index>0 else '(none)'))

print('worst 10')
for index in index_sorted[0:10:]:
    print('\t{}\t{}'.format(param[index], features[index-1].strip() if index>0 else '(none)'))
