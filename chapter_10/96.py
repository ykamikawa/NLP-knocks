# 国名に関するベクトルの抽出
import pickle
from collections import OrderedDict
from scipy import io
import numpy as np

dict_index_t_name = '../data/dict_index_t'
matrix_x300_name = '../data/matrix_x300'
countries_name = '../data/countries.txt'

dict_new_name = '../data/dict_index_country'
matrix_new_name = '../data/matrix_x300_country'


# 辞書読み込み
with open(dict_index_t_name, 'rb') as f:
        dict_index_t = pickle.load(f)

# 行列読み込み
matrix_x300 = io.loadmat(matrix_x300_name)['matrix_x300']

# 辞書にある用語のみの行列を作成
dict_new = OrderedDict()
matrix_new = np.empty([0, 300], dtype=np.float64)
count = 0

with open(countries_name, 'rt') as f:
    for line in f:
        try:
            word = line.strip().replace(' ', '_')
            index = dict_index_t[word]
            matrix_new = np.vstack([matrix_new, matrix_x300[index]])
            dict_new[word] = count
            count += 1
        except:
            pass

# 結果の書き出し
io.savemat(matrix_new_name, {'matrix_x300': matrix_new})
with open(dict_new_name, 'wb') as f:
    pickle.dump(dict_new, f)
