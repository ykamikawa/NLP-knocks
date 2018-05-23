#!/usr/local/bin/zsh

# 3カラム目を数値として逆順ソート
sort ../data/hightemp.txt --key=3,3 --numeric-sort --reverse > ../data/result_test.txt

# Pythonのプログラムで実行
python 18.py > ../data/result.txt

# 結果の確認
diff --report-identical-files ../data/result.txt ../data/result_test.txt
