#!/usr/local/bin/zsh

# マージ
paste ../data/col1.txt ../data/col2.txt > ../data/13_test.txt

# 比較
diff -s ../data/13.txt ../data/13_test.txt
