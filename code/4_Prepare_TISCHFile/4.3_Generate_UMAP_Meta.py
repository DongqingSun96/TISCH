# -*- coding: utf-8 -*-
# @Author: Dongqing Sun
# @E-mail: Dongqingsun96@gmail.com
# @Date:   2020-07-12 13:32:24
# @Last Modified by:   Dongqing Sun
# @Last Modified time: 2020-07-12 13:35:35


from MAESTRO.scATAC_H5Process import read_10X_h5
from adjustText import adjust_text
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib
import os
import json


# without title
DefaulfColorPalette = [
    "#E58606", "#5D69B1", "#52BCA3", "#99C945", "#CC61B0", "#24796C",
    "#DAA51B", "#2F8AC4", "#764E9F", "#ED645A", "#A5AA99", "#BCBD22",
    "#B279A2", "#EECA3B", "#17BECF", "#FF9DA6", "#778AAE", "#1B9E77",
    "#A6761D", "#526A83", "#B82E2E", "#80B1D3", "#68855C", "#D95F02",
    "#BEBADA", "#AF6458", "#D9AF6B", "#9C9C5E", "#625377", "#8C785D",
    "#88CCEE", "#E73F74", "#FFFFB3", "#CCEBC5", "#332288", "#A65628"
]
path = "/home1/wangchenfei/Project/SingleCell/WebServer/TISCH/static/data"
path = "/home/ubuntu/projects/TISCH/static/data"
path = "/home1/wangchenfei/Project/TIRA/TISCH_data_new"

dir_list = os.listdir(path)
dir_list = sorted(dir_list)

sns.set(style="whitegrid", palette="pastel")
sns.set_palette(DefaulfColorPalette)
for i in dir_list:
    umap_file = os.path.join(path, i, "%s_umap.json" %(i))
    png_file = os.path.join(path, i, "%s_umap.png" %(i))
    umap_dict = json.load(open(umap_file, "r"))
    umap_df = pd.DataFrame(umap_dict)
    f, ax = plt.subplots(figsize=(6.5, 6.5))
    cluster_list = []
    text_list = []
    for j, label in enumerate(sorted(list(set(umap_df["Celltype_curated"])))):
        #add data points 
        points = plt.scatter(x=umap_df.loc[umap_df['Celltype_curated']==label, 'UMAP_1'], 
                    y=umap_df.loc[umap_df['Celltype_curated']==label, 'UMAP_2'], 
                    color=DefaulfColorPalette[j], 
                    alpha=1, s = 1)
        cluster_list.append(points)
        #add label
        texts = plt.annotate(label, 
                     umap_df.loc[umap_df['Celltype_curated']==label,['UMAP_1','UMAP_2']].mean(),
                     horizontalalignment='center',
                     verticalalignment='center',
                     size=15, color='black')
        text_list.append(texts)
    # text_list_adjust = []
    # for ind in [2,3,6]:
    #     text_list_adjust.append(text_list[ind])
    # adjust_text(text_list_adjust)
    lgd = plt.legend(cluster_list, sorted(list(set(umap_df["Celltype_curated"]))),bbox_to_anchor=(1.2, 0.5), 
               loc='center', markerscale=8, frameon = False, handletextpad = 0, fontsize = 15)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    plt.box(False)
    plt.savefig(png_file, dpi = 300, bbox_extra_artist=[lgd], bbox_inches = "tight")



# all meta info
DefaulfColorPalette = [
    "#E58606", "#5D69B1", "#52BCA3", "#99C945", "#CC61B0", "#24796C",
    "#DAA51B", "#2F8AC4", "#764E9F", "#ED645A", "#A5AA99", "#BCBD22",
    "#B279A2", "#EECA3B", "#17BECF", "#FF9DA6", "#778AAE", "#1B9E77",
    "#A6761D", "#526A83", "#B82E2E", "#80B1D3", "#68855C", "#D95F02",
    "#BEBADA", "#AF6458", "#D9AF6B", "#9C9C5E", "#625377", "#8C785D",
    "#88CCEE", "#E73F74", "#FFFFB3", "#CCEBC5", "#332288", "#A65628",
    "#0096FF", "#F3D4F4", "#FDCDAC", "#548235", "#9271CB", "#917F1D",
    "#E58606", "#5D69B1", "#52BCA3", "#99C945", "#CC61B0", "#24796C",
    "#DAA51B", "#2F8AC4", "#764E9F", "#ED645A", "#A5AA99", "#BCBD22",
    "#B279A2", "#EECA3B", "#17BECF", "#FF9DA6", "#778AAE", "#1B9E77",
    "#A6761D", "#526A83", "#B82E2E", "#80B1D3", "#68855C", "#D95F02",
    "#BEBADA", "#AF6458", "#D9AF6B", "#9C9C5E", "#625377", "#8C785D",
    "#88CCEE", "#E73F74", "#FFFFB3", "#CCEBC5", "#332288", "#A65628",
    "#0096FF", "#F3D4F4", "#FDCDAC", "#548235", "#9271CB", "#917F1D"
]

path = "/home/ubuntu/projects/TISCH/static/data"
dir_list = os.listdir(path)
dir_list = sorted(dir_list)

sns.set(style="whitegrid", palette="pastel")
sns.set_palette(DefaulfColorPalette)
for i in dir_list:
    umap_file = os.path.join(path, i, "%s_umap.json" %(i))
    umap_dict = json.load(open(umap_file, "r"))
    umap_df = pd.DataFrame(umap_dict)
    for annotation_level in umap_df.columns.tolist()[3:]:
        png_file = os.path.join(path, i, "%s_umap_%s.png" %(i, annotation_level))
        f, ax = plt.subplots(figsize=(6.5, 6.5))
        cluster_list = []
        text_list = []
        annotation_unique  = sorted(list(set(umap_df[annotation_level])))
        if annotation_level == "Cluster":
            annotation_unique_number = [int(i) for i in annotation_unique]
            df = pd.DataFrame({"Cluster": annotation_unique, "Cluster_num": annotation_unique_number})
            df = df.sort_values(by=['Cluster_num'])
            annotation_unique = df["Cluster"].tolist()
        annotation_unique_len = [len(annotation) for annotation in annotation_unique]
        annotation_unique_len_avg = np.mean(annotation_unique_len)
        if len(annotation_unique) <= 20:
            ncol = 1
            anchor_x = 1.2
            if annotation_level in ["Celltype_general", "Celltype_curated", "Celltype_subtype", "Celltype_paper"]:
                anchor_x = 1.3
            if annotation_unique_len_avg > 12:
                anchor_x = 1.3
        elif len(annotation_unique) <= 40:
            ncol = 2
            anchor_x = 1.4
            if annotation_level == "Cluster":
                anchor_x = 1.25
            if annotation_unique_len_avg > 12:
                anchor_x = 1.5
        else:
            ncol = 3
            anchor_x = 1.7
            if annotation_level == "Cluster":
                anchor_x = 1.4
            if annotation_unique_len_avg > 12:
                anchor_x = 1.9
        if annotation_level == "Celltype_general":
            legend_title = "Celltype (malignancy)"
        elif annotation_level == "Celltype_curated":
            legend_title = "Celltype (major-lineage)"
        elif annotation_level == "Celltype_subtype":
            legend_title = "Celltype (minor-lineage)"
        elif annotation_level == "Celltype_paper":
            legend_title = "Celltype (original)"
        else:
            legend_title = annotation_level
        for j, label in enumerate(annotation_unique):
            #add data points 
            points = plt.scatter(x=umap_df.loc[umap_df[annotation_level]==label, 'UMAP_1'], 
                        y=umap_df.loc[umap_df[annotation_level]==label, 'UMAP_2'], 
                        color=DefaulfColorPalette[j], 
                        alpha=1, s = 1)
            cluster_list.append(points)
            #add label
            texts = plt.annotate(label, 
                         umap_df.loc[umap_df[annotation_level]==label,['UMAP_1','UMAP_2']].mean(),
                         horizontalalignment='center',
                         verticalalignment='center',
                         size=15, color='black')
            text_list.append(texts)
        adjust_text(text_list)
        lgd = plt.legend(cluster_list, annotation_unique, bbox_to_anchor=(anchor_x, 0.5), 
                   loc='center', markerscale=8, frameon = False, handletextpad = 0, fontsize = 12,
                   ncol = ncol, title = legend_title, title_fontsize = 14)
        lgd._legend_box.align = "left"
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        plt.box(False)
        plt.title(label = i, fontsize = 22, pad = 20)
        plt.savefig(png_file, dpi = 300, bbox_extra_artist=[lgd], bbox_inches = "tight")
        plt.close(f)
        plt.clf()

