#!/bin/bash

###script of generating prerank files from single cell DE analysis and run GSEA on KEGG and hallmark

gsea_path="/mnt/Storage2/home/wangjin/tools/gsea/GSEA_Linux_4.0.3/"
hs_hallmark_gmt="/mnt/Storage2/home/wangjin/tools/gsea/GSEA_Linux_4.0.3/h.all.v7.1.symbols.gmt"
hs_kegg_gmt="/mnt/Storage2/home/wangjin/tools/gsea/GSEA_Linux_4.0.3/c2.cp.kegg.v7.1.symbols.gmt"
mm_hallmark_gmt="/mnt/Storage2/home/wangjin/tools/gsea/GSEA_Linux_4.0.3/h.all.v7.1.symbols_mouse.gmt"
mm_kegg_gmt="/mnt/Storage2/home/wangjin/tools/gsea/GSEA_Linux_4.0.3/c2.cp.kegg.v7.1.symbols_mouse.gmt"

###split DE analysis results into cell types and generate preranked rnk file
echo "generating rnk file"
cd ${1}
name=$(echo ${1}"_")
# awk -F "\t" -v condition=${2} 'NR!=1{gsub(/ /,"",$7);print>condition"_"$7}' ${2}_tmp; 
for file in $(ls | grep ${2}.*DE.txt$); do fname=$(echo $file | sed "s/${name}//g");awk 'NR!=1{print $6"\t"$2}' OFS="\t" $file | sort -k2gr > $fname"_preranked.rnk"; done

###GSEA analysis for each rnk file using hallmark and kegg gene sets
mkdir -p ${1}_${2}_DE_GSEA/hallmark
mkdir -p ${1}_${2}_DE_GSEA/kegg

for rnk in $(ls | grep preranked.rnk | grep ^${2})
do 
if echo ${1} | grep "mouse"; then
	echo "$rnk for GSEA using $hallmark_gmt";
	$gsea_path/gsea-cli.sh GSEAPreranked -rnk $rnk -gmx $mm_hallmark_gmt -rpt_label $rnk"_hallmark" -out ./ > gsea.log
	echo "$rnk for GSEA using $kegg_gmt"
	$gsea_path/gsea-cli.sh GSEAPreranked -rnk $rnk -gmx $mm_kegg_gmt -rpt_label $rnk"_kegg" -out ./ >> gsea.log
else
	echo "$rnk for GSEA using $hallmark_gmt";
	$gsea_path/gsea-cli.sh GSEAPreranked -rnk $rnk -gmx $hs_hallmark_gmt -rpt_label $rnk"_hallmark" -out ./ > gsea.log
	echo "$rnk for GSEA using $kegg_gmt"
	$gsea_path/gsea-cli.sh GSEAPreranked -rnk $rnk -gmx $hs_kegg_gmt -rpt_label $rnk"_kegg" -out ./ >> gsea.log
fi
done

####merger hallmark results for all cell types
echo "merge all hallmark gsea reports of cell types together "
for file in $(find ./${2}*hallmark* -name "gsea_report_for_na_*xls")
do 
prefix=$(echo $file | awk  -F "_" '{print $1"_"$2"_"$3}');
fname=$(basename ${file}); 
cp $file ./${1}_${2}_DE_GSEA/hallmark/$prefix"_hallmark_"$fname; 
done

####merger kegg results for all cell types
echo "merge all kegg gsea reports of cell types together "
for file in $(find ./${2}*kegg* -name "gsea_report_for_na_*xls")
do 
prefix=$(echo $file | awk  -F "_" '{print $1"_"$2"_"$3}');
fname=$(basename ${file}); 
cp $file ./${1}_${2}_DE_GSEA/kegg/$prefix"_kegg_"$fname; 
done

###delete temporary file
# rm ${2}_tmp   



