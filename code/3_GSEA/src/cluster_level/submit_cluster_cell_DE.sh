#!/bin/bash


cat DE_input.tmp | while read input output 
do
while true
do
sleep 3s
CURRENT=$(ps -u wangjin | grep -E "R" | wc -l)
if [ ${CURRENT} -lt 10 ];then
mkdir -p $output
nohup Rscript cluster_cell_DE.R --input $input --output $output &
break
fi
done
done
