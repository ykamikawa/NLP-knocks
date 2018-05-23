# ファイルをN分割する
import math

n = int(input('N--> '))
file_name = '../data/hightemp.txt'

with open(file_name) as f:
    lines = f.readlines()

count = len(lines)
# 1ファイル当たりの行数
unit = math.ceil(count / n)

for i, offset in enumerate(range(0, count, unit), 1):
    with open('../data/subset_0{}.txt'.format(i), 'w') as f:
        for line in lines[offset:offset + unit]:
            f.write(line)
