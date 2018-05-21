# 集合
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

target1 = "paraparaparadise"
target2 = "paragraph"

set_1 = set(n_gram(target1, n=2))
set_2 = set(n_gram(target2, n=2))

# 和集合
set_or = set_1.union(set_2)
print("和集合: ", set_or)

# 積集合
set_and = set_1.intersection(set_2)
print("積集合: ", set_and)

# 差集合
set_sub = set_1.difference(set_2)
print("差集合: ", set_sub)

# "seが含まれるか?"
print("seがparaparaparadiseに含まれる: ", "se" in set_1)
print("seがparagraphに含まれる: ", "se" in set_2)
