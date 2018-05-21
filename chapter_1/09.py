# Typoglycemia
import random

def Typoglycemia(target):
    """
    Typoglycemia
    スペースで区切られた文字列に対して,各単語の先頭と末尾の文字を残し,
    それ以外の文字の順序をランダムに並び替える
    ただし,長さが4以下の場合は並び替えない
    """
    result = []
    for word in target.split(" "):
        if len(word) <= 4:
            result.append(word)
        else:
            chr_list = list(word[1:-1])
            random.shuffle(chr_list)
            word = word[0] + "".join(chr_list) + word[-1]
            result.append(word)
    return " ".join(result)

# テスト
target = input("文字列を入力してください\n")

result = Typoglycemia(target)
print("実行結果: ", result)
