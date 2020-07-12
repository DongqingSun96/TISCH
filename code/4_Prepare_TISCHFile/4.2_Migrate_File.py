# -*- coding: utf-8 -*-
# @Author: Dongqing Sun
# @E-mail: Dongqingsun96@gmail.com
# @Date:   2020-07-12 13:54:23
# @Last Modified by:   Dongqing Sun
# @Last Modified time: 2020-07-12 13:56:34


import os, shutil

source_path = "/home1/wangchenfei/Project/TIRA/scTumor_Data"
dest_path = "/home1/wangchenfei/Project/TIRA/TISCH_data_new"
dir_list = os.listdir(source_path)
dir_list = sorted(dir_list)
for i in dir_list[0:1]:
    file_list = os.listdir(os.path.join(source_path, i))
    file_need = []
    for j in file_list:
        if j.endswith("_umap.json"):
            file_need.append(j)
        if j.endswith("_genes.tsv"):
            file_need.append(j)
        if j.endswith("_gene_count.h5"):
            file_need.append(j)
        if j.endswith("_expression_Celltype_curated.txt"):
            file_need.append(j)
        if j.endswith("_expression_Celltype_general.txt"):
            file_need.append(j)
        if j.endswith("_expression_Celltype_subtype.txt"):
            file_need.append(j)
        if j.endswith("_expression_Cluster.txt"):
            file_need.append(j)
        if j.endswith("_AllDiffGenes.tsv"):
            file_need.append(j)
    file_need = sorted(file_need)
    m = 0
    while m < int(len(file_need)/8):
        dataset_name = file_need[m*8].split("_AllDiffGenes.tsv")[0]
        target_path = os.path.join(dest_path, dataset_name)
        if os.path.exists(target_path):
            pass
        else:
            os.makedirs(target_path)
        for n in range(8):
            source_file = os.path.join(source_path, i, file_need[m*8 + n])
            shutil.copy(source_file, target_path)
        m = m + 1

