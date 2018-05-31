# 学習
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


result_name = '../data/result.txt'
work_name = '../data/work.txt'


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


# 結果読み込み,予測確率は元の値
results = []
with open(result_name) as f:
    for line in f:
        # タブ区切り
        cols = line.split('\t')
        if len(cols) < 3:
            continue
        # 正解ラベル
        label = cols[0]

        # 識別関数predict()の値
        if cols[1] == '-1':
            # 確率を戻す
            predict = 1.0 - float(cols[2])
        else:
            predict = float(cols[2])
        results.append((label, predict))

# 閾値を変えながらスコア算出,グラフ描画用の配列へセット
thresholds = []
accuracys = []
precisions = []
recalls = []
f1s = []
for threshold in np.arange(0.02, 1.0, 0.02):
    # score()を使うため、一時ファイルに結果保存
    with open(work_name, 'w') as f:
        for label, predict in results:
            if predict > threshold:
                f.write('{}\t{}\t{}\n'.format(label, '+1', predict))
            else:
                f.write('{}\t{}\t{}\n'.format(label, '-1', 1 - predict))

    # スコア算出
    accuracy, precision, recall, f1 = score(work_name)

    # 結果追加
    thresholds.append(threshold)
    accuracys.append(accuracy)
    precisions.append(precision)
    recalls.append(recall)
    f1s.append(f1)

# fontの設定
font = {"family": "AppleGothic"}
mpl.rc("font", **font)

# 折線グラフの値の設定
plt.plot(thresholds, accuracys, color='green', linestyle='--', label='正解率')
plt.plot(thresholds, precisions, color='red', linewidth=3, label='適合率')
plt.plot(thresholds, recalls, color='blue', linewidth=3, label='再現率')
plt.plot(thresholds, f1s, color='magenta', linestyle='--', label='F1スコア')

# 軸の値の範囲の調整
plt.xlim(xmin=0, xmax=1.0)
plt.ylim(ymin=0, ymax=1.0)

# グラフのタイトル、ラベル指定
# タイトル
plt.title('79. 適合率-再現率グラフの描画')
# x軸ラベル
plt.xlabel('ロジスティック回帰モデルの分類の閾値')
# y軸ラベル
plt.ylabel('精度')

# グリッドを表示
plt.grid(axis='both')

# 凡例表示
plt.legend(loc='lower left')

# 表示
plt.show()
