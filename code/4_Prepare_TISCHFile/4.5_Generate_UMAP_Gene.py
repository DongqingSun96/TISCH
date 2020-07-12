# -*- coding: utf-8 -*-
# @Author: Dongqing Sun
# @E-mail: Dongqingsun96@gmail.com
# @Date:   2020-05-22 17:54:43
# @Last Modified by:   Dongqing Sun
# @Last Modified time: 2020-06-29 12:11:09

from MAESTRO.scATAC_H5Process import read_10X_h5
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib
import os
import json

# generate sequential palette
bottom = [0.83, 0.83, 0.83, 1.0]
top = [0.11, 0.0, 0.52, 1.0]

palettecolors = []
n = 50
sep = [0]*4
for i in range(4):
    sep[i] = (bottom[i] - top[i])/n

for i in range(n+1):
    palettecolors.append([bottom[j]-i*sep[j] for j in range(4)])

palettecolors = np.array(palettecolors)
newcmp = matplotlib.colors.ListedColormap(palettecolors, name='DefaultSequentialPalette')

path = "/home1/wangchenfei/Project/TIRA/TISCH_data_new"
dir_list = os.listdir(path)
dir_list = sorted(dir_list)

for dataset in dir_list[-5:-4]:
    print(dataset)
    out_dir = os.path.join(path, dataset, "Gene")
    os.makedirs(out_dir)
    h5_file = os.path.join(path, "%s/%s_gene_count.h5" %(dataset, dataset))
    umap_file = os.path.join(path, "%s/%s_umap.json" %(dataset, dataset))
    # read umap json file
    umap_dict = json.load(open(umap_file, "r"))
    umap_df = pd.DataFrame(umap_dict)
    # read h5
    mat = read_10X_h5(h5_file)
    rawmatrix = mat.matrix
    features = mat.names.tolist()
    barcodes = mat.barcodes.tolist()
    invalid_gene = "THRA1/BTR"
    if invalid_gene.encode() in features:
        invalid_ind = features.index(invalid_gene.encode())
        gene_ind = list(range(len(features)))
        gene_ind.pop(invalid_ind)
    else:
        gene_ind = range(len(features))
    for i in gene_ind:
        gene = features[i].decode()
        out_file = os.path.join(out_dir, "%s_%s_umap.png" %(dataset, gene))
        gene_exp_list = rawmatrix[i,:].toarray().flatten().tolist() 
        umap_df["Expression"] = gene_exp_list
        # draw the gene umap plot
        sns.set(style="whitegrid")
        f, ax = plt.subplots(figsize=(8, 6.5))
        points = plt.scatter(x=umap_df["UMAP_1"], 
                y=umap_df['UMAP_2'], 
                c = umap_df['Expression'],
                alpha=1, s = 1, cmap=newcmp)
        xlabel = ax.set_xticklabels([])
        ylabel = ax.set_yticklabels([])
        plt.box(False)
        colorbar  = plt.colorbar(aspect = 15)
        ax.grid(linewidth = 0.8, color = "#DBDBDB")
        plottitle = plt.title(label = gene, fontsize = 25, pad = 20)
        plt.savefig(out_file, dpi = 200, bbox_inches = "tight")
        plt.close(f)
        plt.clf()

