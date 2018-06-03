# word2vecによる学習
import pickle
from collections import OrderedDict
import numpy as np
from scipy import io
import word2vec

input_name = '../data/corpus81.txt'
word2vec_output_name = '../data/vectors.txt'
dict_index_t_name = '../data/dict_index_t'
matrix_x300_name = '../data/matrix_x300'

# word2vecでベクトル化
word2vec.word2vec(
        train=input_name,
        output=word2vec_output_name,
        size=300,
        threads=4,
        binary=0)

# その結果を読み込んで行列と辞書を作成
with open(word2vec_output_name, 'rt') as f:
    # 先頭行から用語数と次元を取得
    work = f.readline().split(' ')
    size_dict = int(work[0])
    size_x = int(work[1])

    # 辞書と行列作成
    dict_index_t = OrderedDict()
    matrix_x = np.zeros([size_dict, size_x], dtype=np.float64)

    for i, line in enumerate(f):
        work = line.strip().split(' ')
        dict_index_t[work[0]] = i
        matrix_x[i] = work[1:]

# 結果の書き出し
# 行列
io.savemat(matrix_x300_name, {'matrix_x300': matrix_x})
# 辞書
with open(dict_index_t_name, 'wb') as f:
    pickle.dump(dict_index_t, f)
