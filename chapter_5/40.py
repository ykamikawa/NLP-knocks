# 係り受け解析結果の読み込み(形態素)
import CaboCha


file_name = "../data/neko.txt"
parsed_file = "../data/neko.txt.cabocha"


class Morph():
    """
    形態素クラス
    ・表層系(surface)
    ・基本形(base)
    ・品詞(pos)
    ・品詞再分類1(pos1)
    の4つをkeyとするdictに格納し,lineごとに辞書にlistとして返す
    """
    def __init__(self, surface, base, pos, pos1):
        self.surface = surface
        self.base = base
        self.pos = pos
        self.pos1 = pos1

    def __str__(self):
        """オブジェクトの文字列表現"""
        return "surface[{}]\tbase[{}]\tpos[{}]\tpos1[{}]"\
                .format(self.surface, self.base, self.pos, self.pos1)


def parse_neko():
    """
    「吾輩は猫である」を係り受け解析
    「吾輩は猫である」(neko.txt)を係り受け解析してneko.txt.cabochaとして保存
    """
    with open(file_name, "r") as f, open(parsed_file, "w") as pf:
        cabocha = CaboCha.Parser()
        for line in f:
            pf.write(cabocha.parse(line).toString(CaboCha.FORMAT_LATTICE))


def neko_lines():
    """
    「吾輩は猫である」の係り受け解析の解析結果を生成するgenerator
    「吾輩は猫である」の係り受け解析の解析の結果を順次読み込んで
    1文ずつのMorphクラスのインスタンスのリストを渡す

    戻り値:
    1文のMorphクラスのリスト
    """
    with open(parsed_file, "r") as pf:
        morphs = []
        for line in pf:
            # 1文の終了判定
            if line == "EOS\n":
                yield morphs
                morphs = []
            else:
                # 先頭が*の行は係り受け解析結果なのでスキップ
                if line[0] == "*":
                    continue

                # 表層系はtab区切り,それ以外は","区切りでバラす
                cols = line.split("\t")
                res_cols = cols[1].split(",")

                # Morph作成,リストに追加
                morphs.append(Morph(
                    # surface
                    cols[0],
                    # base
                    res_cols[6],
                    # pos
                    res_cols[0],
                    # pos1
                    res_cols[1]
                    ))

        raise StopIteration


# 係り受け解析
parse_neko()

# 1文ずつリスト作成
for i, morphs in enumerate(neko_lines(), 1):
    # 3文目を表示
    if i == 3:
        for morph in morphs:
            print(morph)
        break
