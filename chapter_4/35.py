# 名詞の連結の抽出
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

            # 品詞細分類1が'句点'なら文の終わりと判定し,morphemeを返す
            if res_cols[1] == '句点':
                yield morphemes
                morphemes = []


# 形態素解析し,neko.txt.mecabとして保存
parse_neko()

# 1文ずつ辞書のリストを取得し抽出
# 出現順リスト,重複あり
list_series_noun = []

for line in neko_lines():
    # 見つけた名詞のリスト
    nouns = []
    for morpheme in line:
        # 名詞ならnounsに追加
        if morpheme['pos'] == '名詞':
            nouns.append(morpheme['surface'])

        # 名詞以外なら,それまでの連続する名詞をlist_series_nounに追加
        else:
            if len(nouns) > 1:
                list_series_noun.append("".join(nouns))
            nouns = []

    # 名詞で終わる行があった場合は、最後の連続する名詞をlist_series_nounに追加
    if len(nouns) > 1:
        list_series_noun.append("".join(nouns))

# 重複除去
series_noun = set(list_series_noun)

# 確認しやすいようlist_series_nounを使って出現順にsortして表示
print(sorted(series_noun, key=list_series_noun.index))
