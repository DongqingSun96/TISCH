#!/bin/bash


cat meta_cluster_DE.tmp | while read input output json meta
do
while true
do
sleep 3s
CURRENT=$(ps -u wangjin | grep -E "R" | wc -l)
if [ ${CURRENT} -lt 10 ];then
mkdir -p $output
nohup Rscript meta_cluster_DE.R --input $input --output $output --json $json --meta $meta > $output".log" &
break
fi
done
done
