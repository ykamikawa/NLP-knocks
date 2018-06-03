# アナロジーデータの準備

input_name = '../data/question-words.txt'
output_name = '../data/family.txt'

with open(input_name, 'rt') as f, open(output_name, 'wt') as f_output:
    target = False
    for line in f:
        if target == True:
            # 対象データの場合は別のセクションになるまで出力
            if line.startswith(': '):
                break
            print(line.strip(), file=f_output)
        elif line.startswith(': family'):
            # 対象データ発見
            target = True
