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
cp ${1}_cluster_DE.txt tmp   
# sed -i "s/Mono\/Macro/Mono-Macro/g" tmp
awk -F "\t" 'NR!=1{print>"cluster_"$7}' tmp; for file in $(ls | grep ^cluster_); do awk -F "\t" '{print $8"\t"$3}' OFS="\t" $file | sort -k2gr > $file"_preranked.rnk"; done


###GSEA analysis for each rnk file using hallmark and kegg gene sets
mkdir -p ${1}_cluster_DE_GSEA/hallmark
mkdir -p ${1}_cluster_DE_GSEA/kegg

for rnk in $(ls | grep preranked.rnk | grep ^cluster_)
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
for file in $(find ./*hallmark* -name "gsea_report_for_na_*xls")
do 
prefix=$(echo $file | awk  -F "_" '{print "cluster_"$2}');
fname=$(basename ${file}); 
cp $file ./${1}_cluster_DE_GSEA/hallmark/$prefix"_hallmark_"$fname; 
done

####merger kegg results for all cell types
echo "merge all kegg gsea reports of cell types together "
for file in $(find ./*kegg* -name "gsea_report_for_na_*xls")
do 
prefix=$(echo $file | awk  -F "_" '{print "cluster_"$2}');
fname=$(basename ${file}); 
cp $file ./${1}_cluster_DE_GSEA/kegg/$prefix"_kegg_"$fname; 
done

###delete temporary file
rm tmp


