#!/usr/local/bin/zsh

# 先頭カラムを切り出し、ソート、重複除去
cut -f 1 ../data/hightemp.txt | sort | uniq > ../data/result_test.txt

# Pythonのプログラムで実行、diffで比較するためにソート
python 17.py | sort > ../data/result.txt

# 結果の確認
diff --report-identical-files ../data/result.txt ../data/result_test.txt

