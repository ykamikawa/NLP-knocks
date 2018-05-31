# 学習
import codecs
import snowballstemmer
import numpy as np


sentiment_name = '../data/sentiment.txt'
feature_name = '../data/feature.txt'
param_name = '../data/param.npy'
f_encoding = 'cp1252'

# ハイパーパラメータ
learning_rate = 6.0
epochs = 1000

# 素性抽出
stemmer = snowballstemmer.stemmer('english')

# ストップワードのリスト  http://xpo6.com/list-of-english-stop-words/ のCSV Formatより
stop_words = (
    'a,able,about,across,after,all,almost,also,am,among,an,and,any,are,'
    'as,at,be,because,been,but,by,can,cannot,could,dear,did,do,does,'
    'either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,'
    'him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,'
    'likely,may,me,might,most,must,my,neither,no,nor,not,of,off,often,'
    'on,only,or,other,our,own,rather,said,say,says,she,should,since,so,'
    'some,than,that,the,their,them,then,there,these,they,this,tis,to,too,'
    'twas,us,wants,was,we,were,what,when,where,which,while,who,whom,why,'
    'will,with,would,yet,you,your').lower().split(',')


def is_stopword(str):
    '''
    文字がストップワードかどうかを返す
    大小文字は同一視する

    戻り値:
    ストップワードならTrue、違う場合はFalse
    '''
    return str.lower() in stop_words


def sigmoid(data_x, param):
    '''
    仮説関数
    data_xに対して,paramを使ってdata_yを予測

    戻り値:
    予測値の行列
    '''
    return 1.0 / (1.0 + np.exp(-data_x.dot(param)))


def cross_entropy(data_x, param, data_y):
    '''
    目的関数
    data_xに対して予測した結果正解との差を算出

    戻り値:
    予測と正解との差
    '''
    # データのサンプル数
    s = data_y.size
    # data_yの予測値
    pred = sigmoid(data_x, param)
    # binary cross entropy
    loss = -(data_y*np.log(pred)) - ((np.ones(s)-data_y)*np.log(np.ones(s)-pred))
    loss = (1/s) * sum(loss)
    return loss


def gradient(data_x, param, data_y):
    '''
    最急降下における勾配の計算

    戻り値:
    paramに対する勾配の行列
    '''
    # データのサンプル数
    s = data_y.size
    # data_yの予測値
    pred = sigmoid(data_x, param)
    grad = (1/s) * (pred - data_y).dot(data_x)
    return grad


def extract_features(data, dict_features):
    '''
    文字から素性を抽出
    文章からdict_featuresに含まれる素性を抽出し,
    dict_features['(素性)']の位置を1とする行列を返す
    先頭要素は固定で1のバイアス項

    戻り値:
    先頭要素と該当素性の位置を+1した行列
    '''
    data_one_x = np.zeros(len(dict_features) + 1, dtype=np.float64)
    # 先頭要素は固定で1素性に対応しない重み用
    data_one_x[0] = 1
    for word in data.split(' '):
        # 前後の空白文字除去
        word = word.strip()

        # ストップワード除去
        if is_stopword(word):
            continue

        # ステミング
        word = stemmer.stemWord(word)

        # 素性のインデックス取得,行列の該当箇所を1
        try:
            data_one_x[dict_features[word]] = 1
        except:
            # dict_featuresにない素性は無視
            pass
    return data_one_x


def load_dict_features():
    '''
    features.txtを読み込み,素性をインデックスに変換するための辞書を作成
    インデックスの値は1ベースで,features.txtにおける行番号と一致

    戻り値:
    素性をインデックスに変換する辞書
    '''
    with codecs.open(feature_name, 'r', f_encoding) as f:
        return {line.strip(): i for i, line in enumerate(f, start=1)}


def create_training_set(sentiments, dict_features):
    '''
    正解データsentimentsから学習対象の行列と,極性ラベルの行列を作成
    学習対象の行例の大きさは正解データのレビュー数×(素性数+1)
    列の値は,各レビューに対して該当素性がある場合は1,なければ0
    列の素性のインデックスはdict_features['(素性)']で決まる
    先頭の列は常に1で,素性に対応しない重みの学習用
    dict_featuresに存在しない素性は無視

    極性ラベルの行列の大きさはレビュー数×1
    肯定的な内容が1,否定的な内容が0

    戻り値:
    学習対象の行列,極性ラベルの行列
    '''

    # 行列を0で初期化
    data_x = np.zeros([len(sentiments), len(dict_features) + 1], dtype=np.float64)
    data_y = np.zeros(len(sentiments), dtype=np.float64)

    for i, line in enumerate(sentiments):

        # 素性抽出
        data_x[i] = extract_features(line[3:], dict_features)

        # 極性ラベル行列のセット
        if line[0:2] == '+1':
            data_y[i] = 1

    return data_x, data_y


def train(data_x, data_y, learning_rate, epochs):
    '''
    ロジスティック回帰の学習

    戻り値:
    学習済みのparam
    '''
    param = np.zeros(data_x.shape[1])
    loss = cross_entropy(data_x, param, data_y)
    print('\t学習開始\tloss:{}'.format(loss))

    for i in range(1, epochs + 1):
        # 勾配計算
        grad = gradient(data_x, param, data_y)
        param -= learning_rate * grad

        # lossとparamの最大調整量を算出して経過表示(100回に1回)
        if i % 100 == 0:
            c = cross_entropy(data_x, param, data_y)
            e = np.max(np.absolute(learning_rate * grad))
            print('\t学習中(#{})\tloss:{}\tE:{}'.format(i, c, e))

    c = cross_entropy(data_x, param, data_y)
    e = np.max(np.absolute(learning_rate * grad))
    print('\t学習完了(#{}) \tloss:{}\tE:{}'.format(i, c, e))
    return param


# 素性辞書の読み込み
dict_features = load_dict_features()

# 学習対象の行列と極性ラベルの行列作成
with codecs.open(sentiment_name, 'r', f_encoding) as f:
    data_x, data_y = create_training_set(list(f), dict_features)

# 学習
print('学習率：{}\t学習繰り返し数：{}'.format(learning_rate, epochs))
param = train(data_x, data_y, learning_rate=learning_rate, epochs=epochs)

# 結果を保存
np.save(param_name, param)
