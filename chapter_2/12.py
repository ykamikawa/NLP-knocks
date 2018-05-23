# 1列目をcol1.txtに2列目をcol2.txtに保存
file_name = "../data/hightemp.txt"
with open(file_name) as f:
    lines = f.readlines()
with open("../data/col1.txt", "w") as f1, \
        open("../data/col2.txt", "w") as f2:
            for line in lines:
                f1.write(line.split("\t")[0] + "\n")
                f2.write(line.split("\t")[1] + "\n")
