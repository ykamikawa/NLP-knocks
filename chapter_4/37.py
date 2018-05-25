# 単語の出現頻度上位10語
import MeCab
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib as mpl


file_name = "../data/neko.txt"
parsed_file = "../data/neko.txt.mecab"

def parse_neko():
    """
    「吾輩は猫である」を形態素解析
    「吾輩は猫である」(neko.txt)を形態素解析してneko.txt.mecabとして保存
    """

    with open(file_name, "r") as f, open(parsed_file, "w") as pf:
        mecab = MeCab.Tagger()
        pf.write(mecab.parse(f.read()))


def neko_lines():
    """
    「吾輩は猫である」の形態素解析結果を生成するgenerator
    「吾輩は猫である」の形態素解析の結果を順次読み込んで
    各形態素を
    ・表層系(surface)
    ・基本形(base)
    ・品詞(pos)
    ・品詞再分類1(pos1)
    の4つをkeyとするdictに格納し,lineごとに辞書にlistとして返す

    戻り値:
    1文の各形態素を辞書化したlist
    """

    with open(parsed_file, "r") as pf:
        morphemes = []
        for line in pf:
            # 表層形はtab区切り,それ以外は','区切りでバラす
            cols = line.split('\t')
            # 区切りがなければ終了
            if(len(cols) < 2):
                raise StopIteration
            res_cols = cols[1].split(',')

            # dict作成、listに追加
            morpheme = {
                'surface': cols[0],
                'base': res_cols[6],
                'pos': res_cols[0],
                'pos1': res_cols[1]
            }
            morphemes.append(morpheme)

            # 品詞細分類1が'句点'なら文の終わりと判定し,morphemeを返す
            if res_cols[1] == '句点':
                yield morphemes
                morphemes = []


# 形態素解析し,neko.txt.mecabとして保存
parse_neko()

# Counterオブジェクトに単語をセット
word_counter = Counter()
for line in neko_lines():
    word_counter.update([morpheme['surface'] for morpheme in line])

# 出現頻度上位10語を取得
size = 10
list_word = word_counter.most_common(size)
print(list_word)

# 単語（x軸用）と出現数（y軸用）のリストに分解
list_zipped = list(zip(*list_word))
words = list_zipped[0]
counts = list_zipped[1]

# fontの設定
font = {"family": "AppleGothic"}
mpl.rc("font", **font)

# 棒グラフのデータ指定
plt.bar(
    # x軸の値（0,1,2...9）
    range(0, size),
    # それに対応するy軸の値
    counts,
    # x軸における棒グラフの表示位置
    align='center')

# x軸のラベルの指定
plt.xticks(
    # x軸の値（0,1,2...9）
    range(0, size),
    # それに対応するラベル
    words)

# x軸の値の範囲の調整
# -1〜10（左右に1の余裕を持たせて見栄え良く）
plt.xlim(xmin=-1, xmax=size)

# グラフのタイトル、ラベル指定
#  タイトルとフォントの設定
plt.title('37. 頻度上位10語')
#  x軸とフォントの設定
plt.xlabel('出現頻度が高い10語')
#  x軸とフォントの設定
plt.ylabel('出現頻度')

# グリッドを表示
plt.grid(axis='y')

# 表示
plt.show()
