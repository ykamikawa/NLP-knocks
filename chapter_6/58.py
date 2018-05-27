# タプルの抽出
import os
import subprocess
import xml.etree.ElementTree as ET
import pydot_ng as pydot


file_name = '../data/nlp.txt'
parsed_file = '../data/nlp.txt.xml'

def parse_nlp():
    '''
    nlp.txtをStanford Core NLPで解析しxmlファイルへ出力
    すでに結果ファイルが存在する場合は実行しない
    '''
    if not os.path.exists(parsed_file):
        # StanfordCoreNLP実行,標準エラーはparse.outへ出力
        subprocess.run(
            'java -cp "/usr/local/lib/stanford-corenlp-full-2013-06-20/*"'
            ' -Xmx2g'
            ' edu.stanford.nlp.pipeline.StanfordCoreNLP'
            ' -annotators tokenize,ssplit,pos,lemma,ner,parse,dcoref'
            ' -file ' + file_name + ' 2>../data/parse.out',
            # shellで実行
            shell=True,
            # エラーチェックあり
            check=True
        )


# nlp.txtを解析
parse_nlp()

# 解析結果のxmlをパース
root = ET.parse(parsed_file)

# sentence列挙,1文ずつ処理
for sentence in root.iterfind('./document/sentences/sentence'):
    # sentenceのid
    sent_id = int(sentence.get('id'))

    # それぞれの語の辞書を作成
    # {述語のidx, 述語のtext}
    dict_pred = {}
    # {述語のidx, 述語とnsubj関係の子のtext（＝主語）}
    dict_nsubj = {}
    # {述語のidx, 述語とdobj関係の子のtext（＝目的語）}
    dict_dobj = {}

    # dependencies列挙
    for dep in sentence.iterfind(
        './dependencies[@type="collapsed-dependencies"]/dep'
    ):

        # 関係チェック
        dep_type = dep.get('type')
        if dep_type == 'nsubj' or dep_type == 'dobj':

            # 述語の辞書に追加
            govr = dep.find('./governor')
            idx = govr.get('idx')
            # 重複するが無害なのでチェックは省略
            dict_pred[idx] = govr.text

            # 主語or目的語の辞書に追加
            if dep_type == 'nsubj':
                dict_nsubj[idx] = dep.find('./dependent').text
            else:
                dict_dobj[idx] = dep.find('./dependent').text

    # 述語を列挙、主語と目的語の両方を持つもののみ出力
    for idx, pred in sorted(dict_pred.items(), key=lambda x: x[0]):
        nsubj = dict_nsubj.get(idx)
        dobj = dict_dobj.get(idx)
        if nsubj is not None and dobj is not None:
            print('{}\t{}\t{}'.format(nsubj, pred, dobj))
