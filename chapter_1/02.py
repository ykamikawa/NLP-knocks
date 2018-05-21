from functools import reduce


# 「パトカー」+「タクシー」=「パタトクカシー」
target1 = "パトカー"
target2 = "タクシー"
result = "".join(reduce(lambda a, b: a + b, zip(target1, target2)))
print(result)
