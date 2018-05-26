# 名詞間の係り受けパスの抽出
import CaboCha
import re
import pydot_ng as pydot


result_file = "../data/result.txt"
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


class Chunk():
    """
    文節クラス
    形態素(Morphオブジェクト)のリスト(morphs)、係り先文節インデックス番号(dst)、
    係り元文節インデックス番号のリスト(srcs)をメンバー変数に持つ
    """

    def __init__(self):
        self.morphs = []
        self.srcs = []
        self.dst = -1

    def __str__(self):
        """オブジェクトの文字列表現"""
        surface = ""
        for morph in self.morphs:
            surface += morph.surface
        return "{}\tsrcs{}\tdst[{}]".format(surface, self.srcs, self.dst)

    def normalized_surface(self):
        '''句読点などの記号を除いた表層系'''
        result = ''
        for morph in self.morphs:
            if morph.pos != '記号':
                result += morph.surface
        return result

    def chk_pos(self, pos):
        '''
        指定した品詞(pos)を含むかチェック
        戻り値:
        品詞を含む場合はTrue
        '''
        for morph in self.morphs:
            if morph.pos == pos:
                return True
        return

    def get_morphs_by_pos(self, pos, pos1=''):
        '''
        指定した品詞(pos),品詞細分類1(pos1)の形態素のリストを返す
        pos1の指定がない場合はposのみで判定する

        戻り値：
        形態素(morph)のリスト,該当形態素がない場合は空のリスト
        '''
        if len(pos1) > 0:
            return [res for res in self.morphs
                    if (res.pos == pos) and (res.pos1 == pos1)]
        else:
            return [res for res in self.morphs if res.pos == pos]

    def get_kaku_prt(self):
        '''
        助詞を一つ返す

        戻り値:
        助詞,ない場合はから文字列
        '''
        prts = self.get_morphs_by_pos('助詞')
        if len(prts) > 1:
            # 二つ以上助詞がある場合は,各助詞を優先
            kaku_prts = self.get_morphs_by_pos('助詞', '格助詞')
            if len(kaku_prts):
                prts = kaku_prts

        if len(prts) > 0:
            # 最後を返す
            return prts[-1].surface
        else:
            return ''

    def get_sahen_wo(self):
        '''
        「サ変接続名詞+を」を含む場合は,その部分の表層系を返す

        戻り値:
        「サ変接続名詞+を」の文字列,なければから文字
        '''
        for i, morph in enumerate(self.morphs[0:-1]):
            if (morph.pos == '名詞') \
                    and (morph.pos1 == 'サ変接続') \
                    and (self.morphs[i + 1].pos == '助詞') \
                    and (self.morphs[i + 1].surface == 'を'):
                return morph.surface + self.morphs[i + 1].surface

        return ''

    def noun_masked_surface(self, mask, dst=False):
        '''
        名詞を指定文字(mask)でマスクした表層形を返す
        dstがTrueの場合は最左の名詞をマスクした以降は切り捨てて返す

        戻り値：
        名詞をマスクした表層形
        '''
        result = ''
        for morph in self.morphs:
            if morph.pos != '記号':
                if morph.pos == '名詞':
                    result += mask
                    if dst:
                        return result
                    # 最初に見つけた名詞をマスク、以降の名詞は除去
                    mask = ''
                else:
                    result += morph.surface
        return result


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
    1文ずつのChunkクラスのインスタンスのリストを渡す

    戻り値:
    1文のChunkクラスのリスト
    """
    with open(parsed_file) as pf:
        # idxをkeyにChunkを格納
        chunks = dict()
        idx = -1

        for line in pf:
            # 1文の終了判定
            if line == 'EOS\n':
                # Chunkのリストを返す
                if len(chunks) > 0:
                    # chunksをkeyでソートし、valueのみ取り出し
                    sorted_tuple = sorted(chunks.items(), key=lambda x: x[0])
                    yield list(zip(*sorted_tuple))[1]
                    chunks.clear()

                else:
                    yield []

            # 先頭が*の行は係り受け解析結果なので,Chunkを作成
            elif line[0] == '*':
                # Chunkのインデックス番号と係り先のインデックス番号取得
                cols = line.split(' ')
                idx = int(cols[1])
                dst = int(re.search(r'(.*?)D', cols[2]).group(1))

                # Chunkを生成(なければ)し,係り先のインデックス番号セット
                if idx not in chunks:
                    chunks[idx] = Chunk()
                chunks[idx].dst = dst

                # 係り先のChunkを生成(なければ)し,係り元インデックス番号追加
                if dst != -1:
                    if dst not in chunks:
                        chunks[dst] = Chunk()
                    chunks[dst].srcs.append(idx)
            # それ以外の行は形態素解析結果なので,Morphを作りChunkに追加
            else:
                # 表層形はtab区切り,それ以外は','区切りでバラす
                cols = line.split('\t')
                res_cols = cols[1].split(',')

                # Morph作成,リストに追加
                chunks[idx].morphs.append(
                    Morph(
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


def graph_from_edges_ex(edge_list, directed=False):
    '''
    pydot_ng.graph_from_edges()のノード識別子への対応版

    graph_from_edges()のedge_listで指定するタプルは
    識別子とグラフ表示時のラベルが同一のため、
    ラベルが同じだが実体が異なるノードを表現することができない。
    例えば文の係り受けをグラフにする際、文の中に同じ単語が
    複数出てくると、それらのノードが同一視されて接続されてしまう。

    この関数ではedge_listとして次の書式のタプルを受け取り、
    ラベルが同一でも識別子が異なるノードは別ものとして扱う。

    edge_list = [((識別子1,ラベル1),(識別子2,ラベル2)), ...]

    識別子はノードを識別するためのもので表示されない。
    ラベルは表示用で、同じでも識別子が異なれば別のノードになる。

    なお、オリジナルの関数にあるnode_prefixは未実装。

    戻り値：
    pydot.Dotオブジェクト
    '''

    if directed:
        graph = pydot.Dot(graph_type='digraph')

    else:
        graph = pydot.Dot(graph_type='graph')

    for edge in edge_list:

        id1 = str(edge[0][0])
        label1 = str(edge[0][1])
        id2 = str(edge[1][0])
        label2 = str(edge[1][1])

        # ノード追加
        graph.add_node(pydot.Node(id1, label=label1))
        graph.add_node(pydot.Node(id2, label=label2))

        # エッジ追加
        graph.add_edge(pydot.Edge(id1, id2))

    return graph


# 係り受け解析
parse_neko()

# 結果ファイル作成
with open(result_file, mode='w') as f:
    # 1文ずつリスト作成
    for chunks in neko_lines():
        # 名詞を含むchunkに限定した、chunksにおけるインデックスのリストを作成
        indexs_noun = [i for i in range(len(chunks))
                if len(chunks[i].get_morphs_by_pos('名詞')) > 0]
        # 2つ以上ある
        if len(indexs_noun) < 2:
            continue
        # 名詞を含むchunkの組み合わせを総当りでチェック
        for i, index_x in enumerate(indexs_noun[:-1]):
            for index_y in indexs_noun[i + 1:]:

                meet_y = False
                # XとYの経路がぶつかったchunkのindex
                index_dup = -1
                # Xの経路チェック用
                routes_x = set()

                # 名詞Xから根に向かって,Yにぶつからないか調べながら探索
                dst = chunks[index_x].dst
                while dst != -1:
                    if dst == index_y:
                        # Yにぶつかった
                        meet_y = True
                        break
                    # 経路チェックのために保存
                    routes_x.add(dst)
                    dst = chunks[dst].dst

                # 名詞Yから根まで,Xの経路にぶつからないか調べながら探索
                if not meet_y:
                    dst = chunks[index_y].dst
                    while dst != -1:
                        if dst in routes_x:
                            # Xの経路とぶつかった
                            index_dup = dst
                            break
                        else:
                            dst = chunks[dst].dst

                # 結果出力
                if index_dup == -1:

                    # XからYにぶつかるパターン
                    f.write(chunks[index_x].noun_masked_surface('X'))
                    dst = chunks[index_x].dst
                    while dst != -1:
                        if dst == index_y:
                            f.write(
                                    ' -> ' + chunks[dst].noun_masked_surface('Y', True))
                            break
                        else:
                            f.write(
                                    ' -> ' + chunks[dst].normalized_surface())
                        dst = chunks[dst].dst
                    f.write('\n')

                else:

                    # 経路上の共通のchunkでぶつかるパターン

                    # Xからぶつかる手前までを出力
                    f.write(chunks[index_x].noun_masked_surface('X'))
                    dst = chunks[index_x].dst
                    while dst != index_dup:
                        f.write(' -> ' + chunks[dst].normalized_surface())
                        dst = chunks[dst].dst
                    f.write(' | ')

                    # Yからぶつかる手前までを出力
                    f.write(chunks[index_y].noun_masked_surface('Y'))
                    dst = chunks[index_y].dst
                    while dst != index_dup:
                        f.write(' -> ' + chunks[dst].normalized_surface())
                        dst = chunks[dst].dst
                    f.write(' | ')

                    # ぶつかったchunkを出力
                    f.write(chunks[index_dup].normalized_surface())
                    f.write('\n')
