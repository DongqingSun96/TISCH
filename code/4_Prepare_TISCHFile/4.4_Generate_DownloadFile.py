# -*- coding: utf-8 -*-
# @Author: Dongqing Sun
# @E-mail: Dongqingsun96@gmail.com
# @Date:   2020-07-12 13:36:54
# @Last Modified by:   Dongqing Sun
# @Last Modified time: 2020-07-12 13:53:19


import pandas as pd
import numpy as np
import os
import json

# DE gene table/json
path = "/home/ubuntu/projects/TISCH/static/data"
dir_list = os.listdir(path)
dir_list = sorted(dir_list)

for dataset in dir_list:
    print(dataset)
    diff_gene_file = "./static/data/%s/%s_AllDiffGenes.tsv" %(dataset, dataset)
    umap_file = "./static/data/%s/%s_umap.json" %(dataset, dataset)
    umap_dict = json.load(open(umap_file, "r"))
    umap_df = pd.DataFrame(umap_dict)
    cluster_annotation_df = umap_df[["Cluster", "Celltype_general", "Celltype_curated", "Celltype_subtype"]]
    cluster_annotation_df = cluster_annotation_df.drop_duplicates()
    cluster_annotation_df["Cluster"] = [int(i) for i in cluster_annotation_df["Cluster"]]
    diff_gene_df = pd.read_csv(diff_gene_file, sep = "\t")
    diff_gene_df = diff_gene_df.merge(cluster_annotation_df, left_on='cluster', right_on='Cluster')
    diff_gene_df = diff_gene_df.iloc[:,[7, 8, 9, 10, 6, 1, 2, 4]]
    diff_gene_df["avg_logFC"] = diff_gene_df["avg_logFC"].round(2)
    diff_gene_df["pct.1"] = (diff_gene_df["pct.1"]*100).round(2)
    diff_gene_df["p_val_adj"] = diff_gene_df["p_val_adj"].map(lambda x: "%.3g" % x)
    diff_gene_list = diff_gene_df.values.tolist()
    diff_gene_dict = {"data": diff_gene_list}
    diff_gene_umap_file = "./static/data/%s/%s_AllDiffGenes_table.json" %(dataset, dataset)
    json.dump(diff_gene_dict, open(diff_gene_umap_file, "w"))
    diff_gene_df.columns = ["Cluster", "Celltype (malignancy)", "Celltype (major-lineage)", "Celltype (minor-lineage)", "Gene", "log2FC", "Percentage (%)", "Adjusted p-value"]
    diff_gene_umap_file = "./static/data/%s/%s_AllDiffGenes_table.tsv" %(dataset, dataset)
    diff_gene_df.to_csv(diff_gene_umap_file, sep = "\t", index = False)


# Cell-level meta information
path = "/home/ubuntu/projects/TISCH/static/data"
dir_list = os.listdir(path)
dir_list = sorted(dir_list)

for dataset in dir_list:
    print(dataset)
    umap_file = "%s/%s/%s_umap.json" %(path, dataset, dataset)
    umap_dict = json.load(open(umap_file, "r"))
    umap_df = pd.DataFrame(umap_dict)
    columns = umap_df.columns.tolist()
    columns[columns.index("Celltype_general")] = "Celltype (malignancy)"
    columns[columns.index("Celltype_curated")] = "Celltype (major-lineage)"
    columns[columns.index("Celltype_subtype")] = "Celltype (minor-lineage)"
    if "Celltype_paper" in columns:
        columns[columns.index("Celltype_paper")] = "Celltype (original)"
    umap_df.columns = columns
    cell_umap_file = "%s/%s/%s_CellMetainfo_table.tsv" %(path, dataset, dataset)
    umap_df.to_csv(cell_umap_file, sep = "\t", index = False)


# Cluster-level expression matrix
source_path = "/home/ubuntu/projects/TISCH/static/data/"
dir_list = os.listdir(source_path)
dir_list = sorted(dir_list)
for i in dir_list:
    dest_path = os.path.join(source_path, i, "%s_Expression" %(i))
    if os.path.exists(dest_path):
        pass
    else:
        os.makedirs(dest_path)
    object_dir = os.path.join(source_path, i)
    allfiles = os.listdir(object_dir)
    pattern = "\S*_expression_\S*"
    for file in allfiles:
        if re.match(pattern, file):
            shutil.copy(os.path.join(source_path, i, file), dest_path)
        else:
            pass
    expr_path = "%s_Expression" %(i)
    expr_file = "%s_Expression.zip" %(i)
    os.chdir(os.path.join(source_path, i))
    cmd = "zip -r %s %s" %(expr_file, expr_path)
    os.system(cmd)
