# ステミング
import re
import snowballstemmer


file_name = '../data/nlp.txt'


def nlp_lines():
    '''
    nlp.txtを1文ずつ読み込むgenerator
    nlp.txtを読み込んで1文ずつ渡す

    戻り値:
    1文の文字列
    '''
    with open(file_name, 'r') as lines:
        # 文切り出しの正規表現コンパイル
        pattern = re.compile(
            r'''
            (
                ^ # 行頭
                .*? # 任意のn文字,最小マッチ
                [\.|;|:|\?|!] # . or ; or : or ? or !
            )
            \s # 空白文字
            (
                [A-Z].* # 英大文字以降(=次の文以降)
            )
            ''', re.MULTILINE + re.VERBOSE + re.DOTALL)

        for line in lines:
            line = line.strip()
            while len(line) > 0:
                # 行から1文を取得
                match = pattern.match(line)
                if match:
                    # 切り出した文を返す
                    # 先頭の文
                    yield match.group(1)
                    # 次の文以降
                    line = match.group(2)
                else:
                    # 区切りがないので,最後までが1文
                    yield line
                    line = ''

def nlp_words():
    '''
    nlp.txtを1単語ずつ返すgenerator
    文の終わりでは空文字を返す

    戻り値:
    1単語,ただし文の終わりでは空文字を返す
    '''
    for line in nlp_lines():
        # 単語に分解,終端の区切り文字は除去うして返す
        for word in line.split(' '):
            yield word.rstrip('.,;:?!')
        # 文の終わりは空文字を返す
        yield ''


# 読み込み
stemmer = snowballstemmer.stemmer('english')
for word in nlp_words():
    # 元の結果とステミング結果を出力
    print('{}\t{}'.format(word, stemmer.stemWord(word)))