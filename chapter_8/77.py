result_name = '../data/result.txt'


def score(fname):
    '''
    結果ファイルからスコア算出
    結果ファイルを読み込んで,正解率,適合率,再現率,F1スコアを返す

    戻り値:
    正解率,適合率,再現率,F1スコア
    '''
    # 結果を読み込んで集計
    TP = 0
    FP = 0
    FN = 0
    TN = 0

    with open(fname) as data_file:
        for line in data_file:
            cols = line.split('\t')

            if len(cols) < 3:
                continue

            if cols[0] == '+1':
                if cols[1] == '+1':
                    TP += 1
                else:
                    FN += 1
            else:
                if cols[1] == '+1':
                    FP += 1
                else:
                    TN += 1

    # 算出
    # 正解率
    accuracy = (TP + TN) / (TP + FP + FN + TN)
    # 適合率
    precision = TP / (TP + FP)
    # 再現率
    recall = TP / (TP + FN)
    # F1スコア
    f1 = (2 * recall * precision) / (recall + precision)
    return accuracy, precision, recall, f1


# スコア算出
accuracy, precision, recall, f1 = score(result_name)
print('正解率 \t{}\n適合率 \t{}\n再現率 \t{}\nF1スコア \t{}'.format(
    accuracy, precision, recall, f1
))
