# 単語/文脈の頻度の計測
from collections import Counter
import pickle

input_name = '../data/context.txt'
counter_tc_name = '../data/counter_tc'
counter_t_name = '../data/counter_t'
counter_c_name = '../data/counter_c'

# Counter作成
counter_tc = Counter()
counter_t = Counter()
counter_c = Counter()

# 1行ずつ処理
work_tc = []
work_t = []
work_c = []
with open(input_name, 'rt') as f:
    for i, line in enumerate(f, start=1):
        line = line.strip()
        tokens = line.split('\t')
        work_tc.append(line)
        work_t.append(tokens[0])
        work_c.append(tokens[1])

        # 1,000,000行単位でCounterに追加
        if i % 1000000 == 0:
            counter_tc.update(work_tc)
            counter_t.update(work_t)
            counter_c.update(work_c)
            work_tc = []
            work_t = []
            work_c = []
            print('{} done.'.format(i))

# 最後の半端分を追加
counter_tc.update(work_tc)
counter_t.update(work_t)
counter_c.update(work_c)

# Counter書き出し
with open(counter_tc_name, 'wb') as f:
    pickle.dump(counter_tc, f)
with open(counter_t_name, 'wb') as f:
    pickle.dump(counter_t, f)
with open(counter_c_name, 'wb') as f:
    pickle.dump(counter_c, f)

print('N={}'.format(i))
