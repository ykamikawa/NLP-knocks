#!/usr/local/bin/zsh

# 1カラム目でソートし、重複除去して件数付きで出力、その結果をソート
cut -f 1 ../data/hightemp.txt | sort | uniq -c | sort --reverse
