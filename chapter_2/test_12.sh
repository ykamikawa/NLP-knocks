#!/usr/local/bin/zsh

# col1の抽出と比較
cut -f 1 ../data/hightemp.txt > ../data/col1_test.txt
diff -s ../data/col1.txt ../data/col1_test.txt

# col2の抽出と比較
cut -f 2 ../data/hightemp.txt > ../data/col2_test.txt
diff -s ../data/col2.txt ../data/col2_test.txt
