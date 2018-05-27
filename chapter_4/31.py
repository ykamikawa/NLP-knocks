# 動詞の表層系の抽出
import MeCab

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

            # 品詞細分類1が'句点'なら文の終わりと判定
            if res_cols[1] == '句点':
                yield morphemes
                morphemes = []


# 形態素解析し，neko.txt.mecabとして保存
parse_neko()

# 形態素解析の結果を行単位で生成するgenerator
lines = neko_lines()

# 確認用の出現順リスト
verbs_test = [morpheme["surface"] for line in lines for morpheme in line if morpheme["pos"] == "動詞"]
# 1文ずつ辞書のリストを取得し動詞を抽出
verbs = set(verbs_test)

# 確認のためverbs_testを使って出現順にsort
print(sorted(verbs, key=verbs_test.index))
#print(verbs_test)