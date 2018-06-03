# Ward法によるクラスタリング
import pickle
from collections import OrderedDict
from scipy import io
import numpy as np

from scipy.cluster.hierarchy import ward, dendrogram
from matplotlib import pyplot as plt

dict_index_t_name = '../data/dict_index_country'
matrix_x300_name = '../data/matrix_x300_country'

# 辞書読み込み
with open(dict_index_t_name, 'rb') as f:
    dict_index_t = pickle.load(f)

# 行列読み込み
matrix_x300 = io.loadmat(matrix_x300_name)['matrix_x300']

# ward法でのクラスタリング
ward = ward(matrix_x300)
print(ward)

# デンドログラム表示
dendrogram(ward, labels=list(dict_index_t.keys()), leaf_font_size=8)
plt.show()
