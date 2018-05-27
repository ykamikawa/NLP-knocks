# Tokennazation
import os
import subprocess
import xml.etree.ElementTree as ET


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

# wordのみ取り出し
for word in root.iter('word'):
    print(word.text)
