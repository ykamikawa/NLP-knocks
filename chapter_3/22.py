# カテゴリ名の抽出
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


# 正規表現のコンパイル
pattern = re.compile(
        r"""
        ^ # 行頭
        .* # 任意の文字0文字以上
        \[\[category:
        ( # キャプチャ対象のグループ開始
        .*? # 任意の文字0文字以上,日貪欲マッチ(貪欲にすると後半の"|"で始まる装飾を巻き込んでしまう)
        ) # グループ終了
        (?: # キャプチャ対象外のグループ開始
        \|.* # "|"に続く0文字以上
        )? # グループ終了,0か1の出現
        \]\]
        .* # 任意の文字0文字以上
        $ # 行末
        """, re.multiline + re.verbose)

# 抽出
result = pattern.findall(extract_UK())

# 結果表示
for line in result:
    print(line)

