#!/usr/local/bin/zsh

# Nを入力
echo -n "N-->"
read n

# 切り出し
head -n $n ../data/hightemp.txt
