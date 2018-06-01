# 文脈の抽出
import random


input_name = '../data/corpus81.txt'
output_name = '../data/context.txt'

# 1行ずつ処理
with open(input_name, 'rt') as f, open(output_name, 'wt') as f_output:
    for i, line in enumerate(f):
        # 1語ずつ処理
        tokens = line.strip().split(' ')
        for j, _ in enumerate(tokens):
            # 単語t
            t = tokens[j]
            # 文脈語d
            d = random.randint(1, 5)

            # 前後d語以内の語の列挙
            for k in range(max(j - d, 0), min(j + d + 1, len(tokens))):
                if j != k:
                    print('{}\t{}'.format(t, tokens[k]), file=f_output)

        # 経過表示
        if i % 10000 == 0:
            print('{} done.'.format(i))
