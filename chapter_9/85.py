# 主成分分析による次元圧縮
from scipy import sparse, io
import sklearn.decomposition

matrix_x_name = '../data/matrix_x'
matrix_x300_name = '../data/matrix_x300'

# 行列読み込み
matrix_x = io.loadmat(matrix_x_name)['matrix_x']

# 300次元に次元圧縮
clf = sklearn.decomposition.TruncatedSVD(300)
matrix_x300 = clf.fit_transform(matrix_x)
io.savemat(matrix_x300_name, {'matrix_x300': matrix_x300})
