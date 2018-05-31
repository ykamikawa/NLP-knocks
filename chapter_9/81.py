# 複合語からなる国名への対処

input_name = '../data/corpus.txt'
output_name = '../data/corpus81.txt'
countries_name = '../data/countries.txt'

set_country = set()
dict_country = {}
with open(countries_name, 'rt') as f:
    for line in f:
        words = line.split(' ')
        if len(words) > 1:
            # 集合に追加
            set_country.add(line.strip())
            # 辞書に追加
            if words[0] in dict_country:
                lengths = dict_country[words[0]]
                if not len(words) in lengths:
                    lengths.append(len(words))
                    lengths.sort(reverse=True)
            else:
                dict_country[words[0]] = [len(words)]

# 1行ずつ処理
with open(input_name, 'rt') as f, open(output_name, 'wt') as f_output:
    for line in f:
        # 1語ずつチェック
        tokens = line.strip().split(' ')
        # 結果のトークン配列
        result = []
        # >0なら複数語の続き
        skip = 0
        for i in range(len(tokens)):
            # 複数語の続きの場合はスキップ
            if skip > 0:
                skip -= 1
                continue

            # 1語目が辞書にあるかどうか
            if tokens[i] in dict_country:
                # 後続の語数を切り取って集合にあるかチェック
                hit = False
                for length in dict_country[tokens[i]]:
                    if ' '.join(tokens[i:i + length]) in set_country:
                        # 複数語の国を発見したので'_'で連結して結果に追加
                        result.append('_'.join(tokens[i:i + length]))
                        # 残りの語はスキップ
                        skip = length - 1
                        hit = True
                        break
                if hit:
                    continue

            # 複数語の国ではないので,そのまま結果に追加
            result.append(tokens[i])

        # 出力
        print(*result, sep=' ', end='\n', file=f_output)
