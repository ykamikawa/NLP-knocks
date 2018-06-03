# アナロジーデータへの適用
import pickle
from collections import OrderedDict
from scipy import io
import numpy as np

dict_index_t_name = '../data/dict_index_t'
matrix_x300_name = '../data/matrix_x300'
input_name = '../data/family.txt'
output_name = '../data/family_out.txt'

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
        # ベクトルのノルムが0だと似ているかどうかの判断不可のため-1を返す
        return -1


# 辞書読み込み
with open(dict_index_t_name, 'rb') as f:
    dict_index_t = pickle.load(f)
keys = list(dict_index_t.keys())

# 行列読み込み
matrix_x300 = io.loadmat(matrix_x300_name)['matrix_x300']

# 評価データ読み込み
with open(input_name, 'rt') as f, open(output_name, 'wt') as f_output:
    for line in f:
        cols = line.split(' ')
        try:
            # ベクトル計算
            vec = matrix_x300[dict_index_t[cols[1]]] \
                    - matrix_x300[dict_index_t[cols[0]]] \
                    + matrix_x300[dict_index_t[cols[2]]]

            # コサイン類似度の一番高い単語を抽出
            dist_max = -1
            index_max = 0
            result = ''
            for i, _ in enumerate(dict_index_t):
                dist = cos_sim(vec, matrix_x300[i])
                if dist > dist_max:
                    index_max = i
                    dist_max = dist

            result = keys[index_max]

        except KeyError:
            # 単語がなければ0文字をコサイン類似度-1で出力
            result = ''
            dist_max = -1

        # 出力
        print('{} {} {}'.format(line.strip(), result, dist_max), file=f_output)
        print('{} {} {}'.format(line.strip(), result, dist_max))
