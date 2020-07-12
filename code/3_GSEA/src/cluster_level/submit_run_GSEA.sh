#!/bin/bash


cat GSEA_input.tmp | while read input 
do
while true
do
sleep 3s
CURRENT=$(ps -u wangjin | grep -E "java" | wc -l)
if [ ${CURRENT} -lt 8 ];then
nohup ./run_cluster_GSEA.sh $input &
break
fi
done
done
