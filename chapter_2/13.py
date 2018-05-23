# col1.txtとcol2.txtをマージ
with open("../data/col1.txt") as f1, \
        open("../data/col2.txt") as f2, \
        open("../data/13.txt", "w") as f3:
            line1 = f1.readlines()
            line2 = f2.readlines()
            for a, b in zip(line1, line2):
                f3.write(a.rstrip() + "\t" + b.rstrip() + "\n")
