# MediaWikiマークアップの除去
import gzip
import json
import re

def extract_UK():
    """
    イギリスに関する記事本文を取得
    戻り値:
    イギリスの記事本文
    """

    file_name = "../data/jawiki-country.json.gz"
    with gzip.open(file_name, "rt") as f:
        for line in f:
            data_json = json.loads(line)
            if data_json["title"] == "イギリス":
                return data_json["text"]

    raise ValueError("イギリスの記事が見つかりません")


def remove_markup(target):
    """
    強調マークアップの除去
    引数:
    target -- 対象の文字列
    戻り値:
    強調マークアップを除去した文字列
    """

    # 強調マークアップの除去
    pattern = re.compile(
            r"""
            \'{2,5} # 2~5個の'
            (.*?) # 任意の1文字以上(対象の文字列)
            (\1) # 1番目のキャプチャと同じ
            """, re.MULTILINE + re.VERBOSE)
    target = pattern.sub(r"\2", target)

    # 内部リンクの除去
    pattern = re.compile(
            r"""
            \[\[ # "[["(マークアップの開始)
            (?: # キャプチャ対象外のグループ開始
                [^|]*? # "|"以外の文字が0文字以上,非貪欲
                \| # "|"
            )*? # グループ終了後,このグループが0以上出現
            ([^|]*?) # キャプチャ対象,"|"以外が0文字以上,非貪欲(表示対象の文字列)
            \]\] # "]]"(マークアップの終了)
            """, re.MULTILINE + re.VERBOSE)
    target = pattern.sub(r"\1", target)

    # Template:Langの除去        {{lang|言語タグ|文字列}}
    pattern = re.compile(
            r'''
            \{\{lang    # '{{lang'（マークアップの開始）
            (?:         # キャプチャ対象外のグループ開始
                [^|]*?  # '|'以外の文字が0文字以上、非貪欲
                \|      # '|'
            )*?         # グループ終了、このグループが0以上出現、非貪欲
            ([^|]*?)    # キャプチャ対象、'|'以外が0文字以上、非貪欲（表示対象の文字列）
            \}\}        # '}}'（マークアップの終了）
            ''', re.MULTILINE + re.VERBOSE)
    target = pattern.sub(r'\1', target)

    # 外部リンクの除去  [http://xxxx] 、[http://xxx xxx]
    pattern = re.compile(
            r'''
            \[http:\/\/ # '[http://'（マークアップの開始）
            (?:         # キャプチャ対象外のグループ開始
                [^\s]*? # 空白以外の文字が0文字以上、非貪欲
                \s      # 空白
            )?          # グループ終了、このグループが0か1出現
            ([^]]*?)    # キャプチャ対象、']'以外が0文字以上、非貪欲（表示対象の文字列）
            \]          # ']'（マークアップの終了）
            ''', re.MULTILINE + re.VERBOSE)
    target = pattern.sub(r'\1', target)

    # <br>、<ref>の除去
    pattern = re.compile(
            r'''
            <           # '<'（マークアップの開始）
            \/?         # '/'が0か1出現（終了タグの場合は/がある）
            [br|ref]    # 'br'か'ref'
            [^>]*?      # '>'以外が0文字以上、非貪欲
            >           # '>'（マークアップの終了）
            ''', re.MULTILINE + re.VERBOSE)
    target = pattern.sub('', target)

    return target


# 基礎情報テンプレートの抽出条件のコンパイル
pattern = re.compile(
        r"""
        ^\{\{基礎情報.*?$ # {{"基礎情報"で始まる行
        (.*?) # キャプチャ対象,任意の0文字以上,非貪欲
        ^\}\}$ # "}}"の行
        """, re.MULTILINE + re.VERBOSE + re.DOTALL)

# 基礎情報テンプレートの抽出
contents = pattern.findall(extract_UK())

# 抽出結果からのフィールド名と値の抽出条件コンパイル
pattern = re.compile(
        r"""
        ^\| # "|"で始まる行
        (.+?) # キャプチャ対象(フィールド名),任意の1文字以上,非貪欲
        \s* # 空白文字0文字以上
        =
        \s* # 空白文字0文字以上
        (.+?) # キャプチャ対象(値),任意の1文字以上,非貪欲
        (?: # キャプチャ対象外のグループ開始
            (?=\n\|) # 改行+"|"の手前(肯定の先読み)
            | (?=\n$) # または,改行+終端の手前(肯定の先読み)
        ) # グループ終了
        """, re.MULTILINE + re.VERBOSE + re.DOTALL)

# フィールド名と値の抽出
fields = pattern.findall(contents[0])

# 辞書のセット
result = {field[0]: remove_markup(field[1]) for field in fields}
# 確認用のフィールド名のリスト
keys_test = [field[0] for field in fields]

# 確認のための表示(確認しやすいようにkeys_testを使ってフィールド名の出現順にソート)
for item in sorted(result.items(), key=lambda field: keys_test.index(field[0])):
    print(item)


