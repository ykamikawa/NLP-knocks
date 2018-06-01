# 単語類似度
import pickle
from collections import OrderedDict
from scipy import io
import numpy as np

dict_index_t_name = '../data/dict_index_t'
matrix_x300_name = '../data/matrix_x300'


def cos_sim(vec_a, vec_b):
    '''
    コサイン類似度の計算
    ベクトルvec_a, vec_bのコサイン類似度を求める

    戻り値:
    コサイン類似度
    '''
    norm_ab = np.linalg.norm(vec_a) * np.linalg.norm(vec_b)
    if norm_ab != 0:
        return np.dot(vec_a, vec_b) / norm_ab
    else:
        # ベクトルのノルムが0だと似ているかどうかの判断ができないので-1
        return -1

# 辞書読み込み
with open(dict_index_t_name, 'rb') as f:
    dict_index_t = pickle.load(f)

# 行列読み込み
matrix_x300 = io.loadmat(matrix_x300_name)['matrix_x300']

# 'United States'と'U.S'のコサイン類似度表示
vec_a = matrix_x300[dict_index_t['United_States']]
vec_b = matrix_x300[dict_index_t['U.S']]

print(cos_sim(vec_a, vec_b))
