# ファイルをN分割する
import math

n = int(input("N-->"))
file_name = "../data/hightemp.txt"

with open(file_name) as f:
    lines = f.readlines()

unit, mod = divmod(len(lines), n)
mod_lines = lines[mod:]
lines = zip(*[iter(lines))] * unit)
with open("subset_{}.txt".format(i), "w") as f:
    for i, line in enumerate(lines):
            f.write("".join(line))
    f.write("".join(mod_lines))
