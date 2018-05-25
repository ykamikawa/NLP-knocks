# 単語の出現頻度のヒストグラム
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

# 出現頻度を全件取得
list_word = word_counter.most_common()

# 出現数のリスト取得
counts = list(zip(*list_word))[1]

# fontの設定
font = {"family": "AppleGothic"}
mpl.rc("font", **font)

# ヒストグラムのデータ指定
plt.hist(
    # データのリスト
    counts,
    # ビンの数
    bins=20,
    # 値の範囲
    range=(1, 20))

# x軸の値の範囲の調整
plt.xlim(xmin=1, xmax=20)

# グラフのタイトル,ラベル指定
plt.title("38. ヒストグラム")
plt.xlabel("出現頻度")
plt.ylabel("単語の種類数")

# グリッドを表示
plt.grid(axis='y')

# 表示
plt.show()
