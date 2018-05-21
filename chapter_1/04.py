# 言語記号
target = "Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can."
first_idx = [0,4,5,6,7,8,14,15,18]
result = dict((word[0], i+1) if i in first_idx else (word[:2], i+1) for i, word in enumerate(target.split(" ")))
print(result)
