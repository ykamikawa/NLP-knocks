# アナロジータスクの正解率の計算

input_name = '../data/family_out.txt'

with open(input_name, 'rt') as f:
    # 1行ずつチェック
    correct = 0
    total = 0

    for line in f:
        cols = line.split(' ')
        total += 1
        if cols[3] == cols[4]:
            correct += 1

# 正解率の表示
print('{} ({}/{})'.format(correct / total, correct, total))
