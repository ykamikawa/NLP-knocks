# 行数のカウント
file_name = "../data/hightemp.txt"
with open(file_name) as f:
    lines = f.readlines()
    print(len(lines), " ", file_name)
