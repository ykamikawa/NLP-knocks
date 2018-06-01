# 単語ベクトルの表示
import pickle
from collections import OrderedDict
from scipy import io
import numpy as np

dict_index_t_name = '../data/dict_index_t'
matrix_x300_name = '../data/matrix_x300'

# 辞書読み込み
with open(dict_index_t_name, 'rb') as f:
    dict_index_t = pickle.load(f)

# 行列
matrix_x300 = io.loadmat(matrix_x300_name)['matrix_x300']

# 'Uniterd States'の単語ベクトル表示
print(matrix_x300[dict_index_t['United_States']])
