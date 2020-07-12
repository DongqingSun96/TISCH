#!/bin/bash



cat GSEA_input.tmp | while read input meta
do
while true
do
sleep 3s
CURRENT=$(ps -u wangjin | grep -E "java" | wc -l)
if [ ${CURRENT} -lt 8 ];then
nohup ./meta_cluster_GSEA.sh $input $meta &
break
fi
done
done

