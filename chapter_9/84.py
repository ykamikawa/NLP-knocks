# 単語文脈行列の作成
import math
import pickle
from collections import Counter
from collections import OrderedDict
from scipy import sparse, io


counter_tc_name = '../data/counter_tc'
counter_t_name = '../data/counter_t'
counter_c_name = '../data/counter_c'
matrix_x_name = '../data/matrix_x'
dict_index_t_name = '../data/dict_index_t'
N = 68043147

# Counter読み込み
with open(counter_tc_name, 'rb') as f:
    counter_tc = pickle.load(f)
with open(counter_t_name, 'rb') as f:
    counter_t = pickle.load(f)
with open(counter_c_name, 'rb') as f:
    counter_c = pickle.load(f)

# {単語, インデックス}の辞書作成
dict_index_t = OrderedDict((key, i) for i, key in enumerate(counter_t.keys()))
dict_index_c = OrderedDict((key, i) for i, key in enumerate(counter_c.keys()))

# 行列作成
size_t = len(dict_index_t)
size_c = len(dict_index_c)
matrix_x = sparse.lil_matrix((size_t, size_c))

# f(t, c)を列挙して処理
for k, f_tc in counter_tc.items():
    if f_tc >= 10:
        tokens = k.split('\t')
        t = tokens[0]
        c = tokens[1]
        # 正の相互情報量
        ppml = max(math.log((N * f_tc) / (counter_t[t] * counter_c[c])), 0)
        matrix_x[dict_index_t[t], dict_index_c[c]] = ppml

# 結果の書き出し
io.savemat(matrix_x_name, {'matrix_x': matrix_x})
with open(dict_index_t_name, 'wb') as f:
    pickle.dump(dict_index_t, f)
