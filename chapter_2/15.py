# 末尾からN行を出力
n = int(input("N-->"))
file_name = "../data/hightemp.txt"
with open(file_name, "r") as f:
    lines = f.readlines()[-n:]
    for line in lines:
        print(line.rstrip())

