# n-gram
def n_gram(target, n):
    """
    指定されたリストからn-gramを作成
    引数:
    target -- 対象
    n -- n-gramのn値
    戻り値:
    gramのリスト
    """
    result = [target[i:i+n] for i in range(0, len(target)-n+1)]
    return result

target = "I am an NLPer"
words_target = target.split(" ")

# 単語bi-gram
result = n_gram(words_target, n=2)
print("word 2-gram: ", result)

# 文字bi-gram
result = n_gram(target, n=2)
print("char 2-gram: ", result)
