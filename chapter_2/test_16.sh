#!/usr/local/bin/zsh

# Nを入力
echo -n "N--> "
read n

# 行数算出wcは行数とファイル名を出力するのでcutで行数のみ切り出し
count=`wc -cmlw ../data/hightemp.txt | cut --f 1 --delimiter=" "`

# 1分割当たりの行数算出,余りがある場合は行数を+1
unit=`expr $count / $n`
remainder=`expr $count % $n`
if [ $remainder -gt 0 ]; then
    unit=`expr $unit + 1`
fi

# 分割
split --lines=$unit --numeric-suffixes=1 --additional-suffix=.txt ../data/hightemp.txt ../data/subset_test_

# 検証
for i in `seq 1 $n`
do
    fname=`printf ../data/subset_%02d.txt $i`
    fname_test=`printf ../data/subset_test_%02d.txt $i`
    diff --report-identical-files $fname $fname_test
  done
