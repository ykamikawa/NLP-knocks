# 各行を3カラム目の数値の順にソート
file_name = "../data/hightemp.txt"
with open(file_name, "r") as f:
    lines = f.readlines()
    lines.sort(key=lambda line: float(line.split("\t")[2]), reverse=True)

for line in lines:
    print(line, end="")
