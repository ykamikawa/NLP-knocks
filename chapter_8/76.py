# ラベル付け
import codecs
import snowballstemmer
import numpy as np


sentiment_name = '../data/sentiment.txt'
feature_name = '../data/feature.txt'
param_name = '../data/param.npy'
result_name = '../data/result.txt'
f_encoding = 'cp1252'

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


# 素性辞書の読み込み
dict_features = load_dict_features()

# 学習結果の読み込み
param = np.load(param_name)

# 学習データを読み込んで予測
with codecs.open(sentiment_name, 'r', f_encoding) as f, open(result_name, 'w') as f_result:
    for line in f:
        # 素性抽出
        data_one_x = extract_features(line[3:], dict_features)

        # 予測,結果出力
        pred = sigmoid(data_one_x, param)
        if pred > 0.5:
            f_result.write('{}\t{}\t{}\n'.format(line[0:2], '+1', pred))
        else:
            f_result.write('{}\t{}\t{}\n'.format(line[0:2], '-1', 1 - pred))
