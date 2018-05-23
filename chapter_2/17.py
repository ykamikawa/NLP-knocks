# 1列目の文字列の異なり
file_name = "../data/hightemp.txt"

with open(file_name) as f:
    lines = f.readlines()
    col_set = {line.split("\t")[0] for line in lines}
for n in col_set:
    print(n)
