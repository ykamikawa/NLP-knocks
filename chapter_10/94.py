# WordSimilarity-353での類似度計算
import pickle
from collections import OrderedDict
from scipy import io
import numpy as np

dict_index_t_name = '../data/dict_index_t'
matrix_x300_name = '../data/matrix_x300'
input_name = '../data/wordsim353/combined.tab'
output_name = '../data/combined_out.tab'

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

# 行列読み込み
matrix_x300 = io.loadmat(matrix_x300_name)['matrix_x300']

# 評価データ読み込み
with open(input_name, 'rt') as f, open(output_name, 'wt') as f_output:
    header = True
    for line in f:
        # 先頭行はスキップ
        if header is True:
            header = False
            continue

        cols = line.split('\t')

        try:
            # コサイン類似度計算
            dist = cos_sim(
                    matrix_x300[dict_index_t[cols[0]]],
                    matrix_x300[dict_index_t[cols[1]]])
        except KeyError:
            # 単語がなければコサイン類似度-1で出力
            dist = -1

        # 出力
        print('{}\t{}'.format(line.strip(), dist), file=f_output)
