# t-SNEによる可視化
import pickle
from collections import OrderedDict
from scipy import io
import numpy as np

from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

dict_index_t_name = '../data/dict_index_country'
matrix_x300_name = '../data/matrix_x300_country'

# 辞書読み込み
with open(dict_index_t_name, 'rb') as f:
    dict_index_t = pickle.load(f)

# 行列読み込み
matrix_x300 = io.loadmat(matrix_x300_name)['matrix_x300']

# t-SNE
t_sne = TSNE(perplexity=30, learning_rate=500).fit_transform(matrix_x300)
print(t_sne)

# KMeansクラスタリング
predicts = KMeans(n_clusters=5).fit_predict(matrix_x300)

# 表示
fig, ax = plt.subplots()
cmap = plt.get_cmap('Set1')
for index, label in enumerate(dict_index_t.keys()):
    cval = cmap(predicts[index] / 4)
    ax.scatter(t_sne[index, 0], t_sne[index, 1], marker='.', color=cval)
    ax.annotate(label, xy=(t_sne[index, 0], t_sne[index, 1]), color=cval)
plt.show()
