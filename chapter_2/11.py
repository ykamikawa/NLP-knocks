# タブをスペースに置換
file_name = "../data/hightemp.txt"
with open(file_name) as f:
    lines = f.readlines()
    print("before")
    print("".join(lines))

    result = [line.replace("\t", " ") for line in lines]
    print("after")
    print("".join(result))
