# コーパスの整形
import bz2


input_name = '../data/enwiki-20150112-400-r100-10576.txt.bz2'
output_name = '../data/corpus.txt'

# 1行ずつ処理
with bz2.open(input_name, 'rt') as f, open(output_name, 'wt') as f_output:
    for line in f:
        # 空白で分解,前後の記号除去
        # 結果のトークン配列
        tokens = []
        for chunk in line.split(' '):
            token = chunk.strip().strip('.,!?;:()[]\'"')
            if len(token) > 0:
                tokens.append(token)

        print(*tokens, sep=' ', end='\n', file=f_output)
