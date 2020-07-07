# Create your tasks here
from MAESTRO.scATAC_H5Process import read_10X_h5
from MAESTRO.scATAC_utility import randomString
from .statannot import add_stat_annotation
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from django import forms
import seaborn as sns
import pandas as pd
import numpy as np
from scipy import stats
import os
import json
import re
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ExtractGeneExpression(h5_file, gene, collapse_mode = "mean"):
    mat = read_10X_h5(h5_file)
    rawmatrix = mat.matrix
    features = mat.names.tolist()
    barcodes = mat.barcodes.tolist()

    if isinstance(gene, str):
        if gene.encode() in features:
            gene_idx = features.index(gene.encode())
            gene_exp = rawmatrix[gene_idx,:].toarray()
            gene_exp_list = gene_exp.flatten().tolist()
        else:
            gene_exp_list = []

    if isinstance(gene, list):
        gene = [i.encode() for i in gene]
        gene = list(set(gene) & set(features))
        if gene:
            gene_idx = [features.index(i) for i in gene]
            gene_exp = rawmatrix[gene_idx,:].toarray()
            if collapse_mode == "mean":
                gene_exp_collapse = np.mean(gene_exp, axis = 0)
            if collapse_mode == "median":
                gene_exp_collapse = np.median(gene_exp, axis = 0)
            gene_exp_list = gene_exp_collapse.flatten().tolist()
        else:
            gene_exp_list = []

    return gene_exp_list


# def GenerateViolinData(gene_exp_list, ident, outpre):

#     gene_exp_series = pd.Series(gene_exp_list)
#     gene_exp_groupby = gene_exp_series.groupby(ident)
#     gene_exp_groupby_list = [(name, list(group)) for name, group in gene_exp_groupby]
#     gene_exp_groupby_dict = dict(gene_exp_groupby_list)

#     out_file = "%s_violin.json" %(outpre)
#     json.dump(gene_exp_groupby_dict, open(out_file, "w"))

#     out_file_return = out_file[1:]

#     return out_file_return

def GenerateViolinData(gene_exp_list, ident, outpre):

    gene_exp_series = pd.Series(gene_exp_list)
    gene_exp_groupby = gene_exp_series.groupby(ident)
    gene_exp_groupby_list = [(name, list(group)) for name, group in gene_exp_groupby]
    gene_exp_groupby_dict = dict(gene_exp_groupby_list)

    out_file = "%s_violin.json" %(outpre)
    json.dump(gene_exp_groupby_dict, open(out_file, "w"))

    out_file_return = out_file.split(BASE_DIR)[1]

    return out_file_return


def GenerateGeneUMAPData(gene_exp_list, umap_dict, outpre):
    gene_umap_dict = umap_dict
    gene_umap_dict["expression"] = gene_exp_list

    out_file = "%s_umap.json" %(outpre)
    df_out_file = "%s_umap.csv" %(outpre)
    json.dump(gene_umap_dict, open(out_file, "w"))

    out_file_return = out_file.split(BASE_DIR)[1]
    df = pd.DataFrame(data = gene_umap_dict)
    df.to_csv(df_out_file)

    return out_file_return


def GenerateGeneUMAPPlot(dataset, gene, gene_label, collapse_mode = "mean"):

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

    h5_file = os.path.join(BASE_DIR, "static/data/%s/%s_gene_count.h5" %(dataset, dataset))
    umap_file = os.path.join(BASE_DIR, "static/data/%s/%s_umap.json" %(dataset, dataset))
    gene_file = os.path.join(BASE_DIR, "static/data/%s/%s_genes.tsv" %(dataset, dataset))
    out_dir = os.path.join(BASE_DIR, "media/tmp/") + randomString()

    # os.makedirs(out_dir)
    if gene_label == "":
        gene_label = "Gene"
    out_pre = "%s_%s_%s" %(out_dir, dataset, gene_label)

    out_file = "%s_umap.png" %(out_pre)
    umap_dict = json.load(open(umap_file, "r"))
    umap_df = pd.DataFrame(umap_dict)

    gene_exp_list = ExtractGeneExpression(h5_file, gene, collapse_mode)

    if gene_exp_list:
        umap_df["Expression"] = gene_exp_list

        sns.set(style="whitegrid")
        # f, ax = plt.subplots(figsize=(8, 6.5))
        # points = plt.scatter(x=umap_df["UMAP_1"], 
        #         y=umap_df['UMAP_2'], 
        #         c = umap_df['Expression'],
        #         alpha=1, s = 1, cmap=newcmp)
        f = plt.figure(figsize=(8, 6.5))
        ax = f.subplots()
        points = ax.scatter(x=umap_df["UMAP_1"], 
                y=umap_df['UMAP_2'], 
                c = umap_df['Expression'],
                alpha=1, s = 1, cmap=newcmp)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        # plt.box(False)
        ax.set_frame_on(False)
        ax.grid(linewidth = 0.8, color = "#DBDBDB")
        ax.set_title(label = gene_label, fontsize = 25, pad = 20)
        f.colorbar(points, ax = ax, aspect = 15)
        # f.title(label = gene_label, fontsize = 25, pad = 20)
        f.savefig(out_file, dpi = 300, bbox_inches = "tight")
        # plt.clf()
        # plt.cla()
        # plt.close()

        plt.close(f)
        f.clf()
        ax.cla()

        # plt.clf()
    else:
        sns.set(style="whitegrid")
        f = plt.figure(figsize=(8, 6.5))
        ax = f.subplots()
        points = ax.scatter(x=umap_df["UMAP_1"], 
                y=umap_df['UMAP_2'], 
                c = "#D4D4D4",
                alpha=1, s = 1)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        # plt.box(False)
        ax.set_frame_on(False)
        # colorbar  = plt.colorbar(matplotlib.cm.ScalarMappable(cmap=newcmp), aspect = 15)
        colorbar  = f.colorbar(matplotlib.cm.ScalarMappable(cmap=newcmp), aspect = 15)
        ax.grid(linewidth = 0.8, color = "#DBDBDB")
        ax.set_title(label = "%s is NOT detected in the dataset" %(gene_label), fontsize = 16, pad = 20)
        # plt.title(label = "%s is NOT detected in the dataset" %(gene_label), fontsize = 16, pad = 20)
        f.savefig(out_file, dpi = 300, bbox_inches = "tight")
        plt.close(f)
        plt.clf()

    out_file_return = out_file.split(BASE_DIR)[1]
    
    return out_file_return


def GeneratePlotData(dataset, gene, collapse_mode = "mean"):

    h5_file = os.path.join(BASE_DIR, "static/data/%s/%s_gene_count.h5" %(dataset, dataset))
    umap_file = os.path.join(BASE_DIR, "static/data/%s/%s_umap.json" %(dataset, dataset))
    out_dir = os.path.join(BASE_DIR, "media/tmp/") + randomString()

    # os.makedirs(out_dir)
    if isinstance(gene, str):
        out_pre = "%s_%s_%s" %(out_dir, dataset, gene)
    if isinstance(gene, list):
        out_pre = "%s_%s_%s" %(out_dir, dataset, "gene")

    umap_dict = json.load(open(umap_file, "r"))
    ident = umap_dict["Celltype_curated"]

    gene_exp_list = ExtractGeneExpression(h5_file, gene, collapse_mode)

    violin_file = GenerateViolinData(gene_exp_list = gene_exp_list, ident = ident, outpre = out_pre)
    # violin_file = GenerateViolinData(gene_exp_list = gene_exp_list, umap_dict = umap_dict, outpre = out_pre)
    gene_umap_file = GenerateGeneUMAPData(gene_exp_list = gene_exp_list, umap_dict = umap_dict, outpre = out_pre)

    return {"violin": violin_file, "gene_umap": gene_umap_file}


def GenerateGeneList(dataset_list):
    dataset = dataset_list[0]
    gene_file = os.path.join(BASE_DIR, "static/data/%s/%s_genes.tsv" %(dataset, dataset))
    genes = open(gene_file, "r").readlines()
    gene_list = [i.strip() for i in genes]
    for dataset in dataset_list[1:]:
        gene_file = os.path.join(BASE_DIR, "static/data/%s/%s_genes.tsv" %(dataset, dataset))
        genes = open(gene_file, "r").readlines()
        genes = [i.strip() for i in genes]
        gene_list = list(set(gene_list) | set(genes))
    gene_list.sort()
    return gene_list


def GenerateHeatmapData(dataset_list, gene, annotation_level):
    human_mouse_gene_match_file = os.path.join(BASE_DIR, "static/commondata/Human_mouse_gene.json")
    mouse_human_gene_match_file = os.path.join(BASE_DIR, "static/commondata/Mouse_human_gene.json")
    human_mouse_gene_dict = json.load(open(human_mouse_gene_match_file, "r"))
    mouse_human_gene_dict = json.load(open(mouse_human_gene_match_file, "r"))
    dataset_list.sort(reverse = True)
    gene_df = pd.DataFrame()
    i = 0
    while i < len(dataset_list):
        dataset = dataset_list[i]
        if "mouse" in dataset:
            if gene.isupper():
                gene_use = human_mouse_gene_dict.get(gene, gene)
            else:
                gene_use = gene
        else:
            if gene.isupper():
                gene_use = gene
            else:
                gene_use = mouse_human_gene_dict.get(gene, gene)

        expr_file = os.path.join(BASE_DIR, "static/data/%s/%s_expression_%s.txt" %(dataset, dataset, annotation_level))
        df = pd.read_csv(expr_file, sep = "\t")
        if gene_use in df.index:
            gene_expr = df.loc[gene_use,]
            gene_df = pd.DataFrame(gene_expr)
            gene_df.columns = [dataset]
            break
        else:
            i += 1

    j = i + 1
    gene_df_list = []
    if j < len(dataset_list):
        for dataset in dataset_list[j:]:
            if "mouse" in dataset:
                if gene.isupper():
                    gene_use = human_mouse_gene_dict.get(gene, gene)
                else:
                    gene_use = gene
            else:
                if gene.isupper():
                    gene_use = gene
                else:
                    gene_use = mouse_human_gene_dict.get(gene, gene)
            expr_file = os.path.join(BASE_DIR, "static/data/%s/%s_expression_%s.txt" %(dataset, dataset, annotation_level))
            df = pd.read_csv(expr_file, sep = "\t")
            if gene_use in df.index:
                gene_expr = df.loc[gene_use,]
                gene_df0 = pd.DataFrame(gene_expr)
                gene_df0.columns = [dataset]
                gene_df_list.append(gene_df0)
            else:
                continue
                
    gene_df_merge = gene_df.join(gene_df_list, how = "outer")
    gene_df_merge = gene_df_merge.sort_index(ascending = True)
    gene_df_merge = gene_df_merge.round(decimals = 2)
    
    # keep the cell-types existing in over one dataset
    # if len(dataset_list) > 1:
    #     notnull_count = pd.notnull(gene_df_merge).apply(np.sum, axis=1)
    #     gene_df_merge = gene_df_merge.loc[notnull_count[notnull_count > 1].index]

    gene_df_merge = gene_df_merge.where(pd.notnull(gene_df_merge), None)
    gene_df_merge = gene_df_merge.T

    gene_dataset_dict = {"expression": gene_df_merge.values.tolist(), "celltype":gene_df_merge.columns.to_list(), "dataset":gene_df_merge.index.to_list()}

    out_dir = os.path.join(BASE_DIR, "media/tmp/") + randomString()
    headmap_file = "%s_%s_dataset_heatmap.json" %(out_dir, gene)
    json.dump(gene_dataset_dict, open(headmap_file, "w"))
    out_file_return = headmap_file.split(BASE_DIR)[1]
    return out_file_return


def GenerateViolinGridGeneData(dataset_list, gene, annotation_level):
    human_mouse_gene_match_file = os.path.join(BASE_DIR, "static/commondata/Human_mouse_gene.json")
    mouse_human_gene_match_file = os.path.join(BASE_DIR, "static/commondata/Mouse_human_gene.json")
    human_mouse_gene_dict = json.load(open(human_mouse_gene_match_file, "r"))
    mouse_human_gene_dict = json.load(open(mouse_human_gene_match_file, "r"))

    dataset_list.sort()
    gene_df = pd.DataFrame()

    i = 0
    ident_list_all = []
    gene_exp_list_all = []
    dataset_list_all = []

    while i < len(dataset_list):
        dataset = dataset_list[i];
        h5_file = os.path.join(BASE_DIR, "static/data/%s/%s_gene_count.h5" %(dataset, dataset))
        umap_file = os.path.join(BASE_DIR, "static/data/%s/%s_umap.json" %(dataset, dataset))
        gene_file = os.path.join(BASE_DIR, "static/data/%s/%s_genes.tsv" %(dataset, dataset))
        genes = open(gene_file, "r").readlines()
        gene_list = [i.strip() for i in genes]
        if "mouse" in dataset:
            if gene.isupper():
                gene_use = human_mouse_gene_dict.get(gene, gene)
            else:
                gene_use = gene
        else:
            if gene.isupper():
                gene_use = gene
            else:
                gene_use = mouse_human_gene_dict.get(gene, gene)
        if gene_use in gene_list:
            umap_dict = json.load(open(umap_file, "r"))
            ident_list = umap_dict[annotation_level]
            gene_exp_list = ExtractGeneExpression(h5_file, gene_use)
            dataset_name_list = [dataset]*len(gene_exp_list)
            ident_list_all = ident_list_all + ident_list
            gene_exp_list_all = gene_exp_list_all + gene_exp_list
            dataset_list_all = dataset_list_all + dataset_name_list
            i = i + 1
        else:
            i = i + 1
            continue

    gene_expr_df = pd.DataFrame({'Expression':gene_exp_list_all, 'Celltype':ident_list_all, 'Dataset':dataset_list_all})

    return gene_expr_df


def ViolinGridGenePlot(gene_df, gene):
    DefaulfColorPalette = ["#E58606", "#5D69B1", "#52BCA3", "#99C945", "#CC61B0", "#24796C",
        "#DAA51B", "#2F8AC4", "#764E9F", "#ED645A", "#A5AA99", "#BCBD22",
        "#B279A2", "#EECA3B", "#17BECF", "#FF9DA6", "#778AAE", "#1B9E77",
        "#A6761D", "#526A83", "#B82E2E", "#80B1D3", "#68855C", "#D95F02",
        "#BEBADA", "#AF6458", "#D9AF6B", "#9C9C5E", "#625377", "#8C785D"]
    out_dir = os.path.join(BASE_DIR, "media/tmp/") + randomString()

    # if len(set(gene_df["Dataset"].tolist())) > 1:
    #     # keep the cell-types existing in over one dataset
    #     celltype_dataset_df = gene_df[["Celltype","Dataset"]]
    #     celltype_dataset_df = celltype_dataset_df.drop_duplicates(keep='first')
    #     celltype_dataset_count_df = celltype_dataset_df.groupby(["Celltype"]).count()
    #     celltypes_common = celltype_dataset_count_df[celltype_dataset_count_df["Dataset"] >1].index.tolist()
    #     gene_df_use = gene_df[gene_df["Celltype"].isin(celltypes_common)]
    # else:
    #     gene_df_use = gene_df
    gene_df_use = gene_df
    celltypes = sorted(list(set(gene_df_use["Celltype"].tolist())))
    datasets = sorted(list(set(gene_df_use["Dataset"].tolist())))

    if len(datasets) == 1:
        height = 6
        aspect = 5
        top = 0.75
        ylabel_size = 25
        xlabel_sixe = 22
        title_size = 30
    elif len(datasets) < 5:
        height = 3
        aspect = 10
        top = 0.8
        ylabel_size = 25
        xlabel_sixe = 22
        title_size = 30
    elif len(datasets) < 10 and len(datasets) >= 5:
        height = 3
        aspect = 15
        top = 0.9
        ylabel_size = 35
        xlabel_sixe = 32
        title_size = 45
    elif len(datasets) < 15 and len(datasets) >= 10:
        height = 2
        aspect = 20
        top = 0.9
        ylabel_size = 35
        xlabel_sixe = 32
        title_size = 45
    elif len(datasets) < 20 and len(datasets) >= 15:
        height = 2
        aspect = 25
        top = 0.9
        ylabel_size = 42
        xlabel_sixe = 40
        title_size = 52
    elif len(datasets) < 50 and len(datasets) >= 20:
        height = 2
        aspect = 25
        top = 0.95
        ylabel_size = 42
        xlabel_sixe = 40
        title_size = 52
    else:
        height = 2
        aspect = 25
        top = 0.96
        ylabel_size = 42
        xlabel_sixe = 40
        title_size = 52
    sns.set(style="whitegrid", palette="pastel")
    g = sns.FacetGrid(gene_df_use, row="Dataset", margin_titles=False, height = height, aspect = aspect, sharex = True, row_order = datasets)
    g = g.map(sns.violinplot, "Celltype", "Expression", order = celltypes, scale="width", cut=0, linewidth = 1.2, palette = DefaulfColorPalette)
    g.set_titles(row_template = '')
    g.set_xlabels(label = '')
    for i in range(len(datasets)):
        ax = g.axes.flatten()[i]
        ax.set_ylabel(ylabel = datasets[i], url = "/data/" + datasets[i], color = "#54aced", fontsize = ylabel_size, rotation = "horizontal", horizontalalignment = "right", verticalalignment = "center")
        for label in ax.get_xticklabels():
            label.set_rotation(315)
            label.set_horizontalalignment("left")
            label.set_fontsize(xlabel_sixe)

    g.fig.tight_layout()
    g.fig.subplots_adjust(top=top)
    g.fig.suptitle(gene, fontsize=title_size)
    g.savefig("%s_%s_violin_multiple.svg" %(out_dir, gene))
    g.savefig("%s_%s_violin_multiple.pdf" %(out_dir, gene))
    plt.close(g.fig)
    # plt.clf()
    # plt.cla()

    svg_text = open("%s_%s_violin_multiple.svg" %(out_dir, gene)).readlines()
    svg_text[4] = re.sub(r'height="[0-9.]+pt" ', '', svg_text[4])
    svg_text[4] = re.sub(r'width="[0-9.]+pt" ', 'width="100%" ', svg_text[4])
    svg_text_embed = ''.join(svg_text[4:])

    pdf_file = "%s_%s_violin_multiple.pdf" %(out_dir, gene)
    pdf_file_return = pdf_file.split(BASE_DIR)[1]

    return (svg_text_embed, pdf_file_return)

def GenerateViolinGridDatasetData(dataset, gene_list, annotation_level, gene_label_list = None, collapse_mode = None):

    h5_file = os.path.join(BASE_DIR, "static/data/%s/%s_gene_count.h5" %(dataset, dataset))
    umap_file = os.path.join(BASE_DIR, "static/data/%s/%s_umap.json" %(dataset, dataset))

    umap_dict = json.load(open(umap_file, "r"))
    group = []
    if isinstance(annotation_level, str):
        annotation = umap_dict[annotation_level]
    if isinstance(annotation_level, list):
        annotation = umap_dict[annotation_level[0]]
        group = umap_dict[annotation_level[1]]

    if collapse_mode:
        gene_exp_list_collapse = ExtractGeneExpression(h5_file, gene_list, collapse_mode)
        if group:
            gene_expr_df = pd.DataFrame({'Expression':gene_exp_list_collapse, annotation_level[0]: annotation, annotation_level[1]: group,'Gene':gene_label_list*len(gene_exp_list_collapse)})
        else:
            gene_expr_df = pd.DataFrame({'Expression':gene_exp_list_collapse, annotation_level: annotation, 'Gene':gene_label_list*len(gene_exp_list_collapse)})

    else:
        mat = read_10X_h5(h5_file)
        rawmatrix = mat.matrix
        features = mat.names.tolist()
        barcodes = mat.barcodes.tolist()

        gene_exp_list_all = []
        gene_list_all = []
        if group:
            annotation_all = annotation*len(gene_list)
            group_all = group*len(gene_list)
        else:
            annotation_all = annotation*len(gene_list)

        i = 0
        while i < len(gene_list):
            gene = gene_list[i]
            gene_idx = features.index(gene.encode())
            gene_exp = rawmatrix[gene_idx,:].toarray()
            gene_exp_list = gene_exp.flatten().tolist()
            gene_exp_list_all = gene_exp_list_all + gene_exp_list
            gene_list_cur = [gene]*len(gene_exp_list)
            gene_list_all = gene_list_all + gene_list_cur
            i = i + 1
        
        if group:
            gene_expr_df = pd.DataFrame({'Expression':gene_exp_list_all, annotation_level[0]: annotation_all, annotation_level[1]: group_all, 'Gene':gene_list_all})
        else:
            gene_expr_df = pd.DataFrame({'Expression':gene_exp_list_all, annotation_level: annotation_all, 'Gene':gene_list_all})

    return gene_expr_df


def ViolinGridDatasetPlot(gene_df, dataset, annotation_level, groupby):
    DefaulfColorPalette = ["#E58606", "#5D69B1", "#52BCA3", "#99C945", "#CC61B0", "#24796C",
        "#DAA51B", "#2F8AC4", "#764E9F", "#ED645A", "#A5AA99", "#BCBD22",
        "#B279A2", "#EECA3B", "#17BECF", "#FF9DA6", "#778AAE", "#1B9E77",
        "#A6761D", "#526A83", "#B82E2E", "#80B1D3", "#68855C", "#D95F02",
        "#BEBADA", "#AF6458", "#D9AF6B", "#9C9C5E", "#625377", "#8C785D"]
    out_dir = os.path.join(BASE_DIR, "media/tmp/") + randomString()

    genes = sorted(list(set(gene_df["Gene"].tolist())))
    annotation = sorted(list(set(gene_df[annotation_level].tolist())))
    
    # if len(genes) == 6:
    #     height = 3
    #     aspect = 12
    #     label_fontsize = 38
    #     title_fontsize = 50
    #     top_per = 0.9
    # if len(genes) == 5:
    #     height = 4
    #     aspect = 10
    #     label_fontsize = 40
    #     title_fontsize = 55
    #     top_per = 0.9
    # if len(genes) == 4:
    #     height = 5
    #     aspect = 8
    #     label_fontsize = 40
    #     title_fontsize = 55
    #     top_per = 0.9
    # if len(genes) == 3:
    #     height = 6
    #     aspect = 7
    #     label_fontsize = 40
    #     title_fontsize = 55
    #     top_per = 0.9
    # if len(genes) == 2:
    #     height = 7
    #     aspect = 6
    #     label_fontsize = 40
    #     title_fontsize = 55
    #     top_per = 0.9
    # if len(genes) == 1:
    #     height = 6
    #     aspect = 5
    #     label_fontsize = 30
    #     title_fontsize = 35
    #     top_per = 0.85

    if len(genes) == 6:
        height = 2.6
        aspect = 12
        label_fontsize = 32
        title_fontsize = 38
        top_per = 0.9
    if len(genes) == 5:
        height = 2.8
        aspect = 10
        label_fontsize = 30
        title_fontsize = 35
        top_per = 0.9
    if len(genes) == 4:
        height = 3
        aspect = 8
        label_fontsize = 25
        title_fontsize = 30
        top_per = 0.9
    if len(genes) == 3:
        height = 4
        aspect = 7
        label_fontsize = 25
        title_fontsize = 30
        top_per = 0.9
    if len(genes) == 2:
        height = 6
        aspect = 6
        label_fontsize = 30
        title_fontsize = 35
        top_per = 0.9
    if len(genes) == 1:
        height = 9
        aspect = 5
        label_fontsize = 20
        title_fontsize = 22
        top_per = 0.85
    
    

    # ratio = 1.3 - 0.1*(len(celltypes)-1)
    # if 0.3 < ratio < 0.7:
    #     ratio = 0.7
    # if 0 < ratio <= 0.3:
    #     ratio = 0.5
    # if -0.4 < ratio <= 0:
    #     ratio = 0.5
    # if -0.7 < ratio <= -0.4:
    #     ratio = 0.4
    # if ratio <= -0.7:
    #     ratio = 0.35
    # aspect = len(celltypes)*ratio*3.5/height
    aspect = (len(annotation)*2.0/15 + 10.0/3)*len(genes)/3
    right_per = len(annotation)*0.1/12 + 0.767
    if len(annotation) <= 4:
        aspect = 4*len(genes)/3
        right_per = 0.8
    if len(annotation) >= 16:
        aspect = 6*len(genes)/3
        right_per = 0.9

    out_file = "%s_%s_violin_multiple_%s_%s.png" %(out_dir, dataset, annotation_level, groupby)
    if groupby == "None":
        sns.set(style="whitegrid")
        g = sns.FacetGrid(gene_df, row="Gene",margin_titles=False, height = height, aspect = aspect, sharex = True, row_order = genes)
        print(list(g.facet_data()))
        # for (row_i, col_j, hue_k), data_ijk in g.facet_data():
        #     ax = g.axes[row_i, col_j]
        #     print(ax)
        #     print((row_i, col_j))
        g = g.map(sns.violinplot, annotation_level, "Expression", order = annotation, scale="width", cut=0, linewidth = 1.2, palette = DefaulfColorPalette)
        # g = sns.catplot(x= annotation_level, y='Expression', data = gene_df,
        #                row='Gene',  kind='violin', margin_titles=False, height = height, 
        #                aspect = aspect, sharex = True, row_order = genes, 
        #                order = annotation, scale="area", cut=0, linewidth = 1.2, palette = DefaulfColorPalette)
        g.set_titles(row_template = '')
        g.set_xlabels(label = '')
        for i in range(len(genes)):
            ax = g.axes.flatten()[i]
            ax.set_ylabel(ylabel = genes[i], fontsize = label_fontsize, rotation = "horizontal", horizontalalignment = "right", verticalalignment = "center")
            for label in ax.get_yticklabels():
                label.set_fontsize(label_fontsize/2)
            for label in ax.get_xticklabels():
                label.set_rotation(315)
                label.set_horizontalalignment("left")
                label.set_fontsize(label_fontsize)
                
        g.fig.tight_layout()
        g.fig.subplots_adjust(top= top_per)
        g.fig.suptitle(dataset, fontsize = title_fontsize)
        g.savefig(out_file, dpi = 200)
        plt.close(g.fig)
        g.fig.clf()
        plt.cla()
        # plt.clf()
        # plt.cla()
        # plt.close()

    else:        
        legends = sorted(list(set(gene_df[groupby].tolist())))
        sns.set(style="whitegrid", palette="Set2")
        g = sns.catplot(x= annotation_level, y='Expression', hue= groupby, data = gene_df,
                       row='Gene',  kind='violin', margin_titles=False, height = height, 
                       aspect = aspect, sharex = True, row_order = genes, hue_order = legends,
                       order = annotation, scale="area", cut=0, linewidth = 1.2, legend = False)
        g.set_titles(row_template = '')
        g.set_xlabels(label = '')
        for i in range(len(genes)):
            ax = g.axes.flatten()[i]
            ax.set_ylabel(ylabel = genes[i], fontsize = label_fontsize, rotation = "horizontal", horizontalalignment = "right", verticalalignment = "center")
            for label in ax.get_xticklabels():
                label.set_rotation(315)
                label.set_horizontalalignment("left")
                label.set_fontsize(label_fontsize)
                
        g.fig.tight_layout()
        g.fig.subplots_adjust(top = top_per)
        # print(right_per)
        # g.fig.subplots_adjust(top= top_per)
        g.fig.suptitle(dataset, fontsize = title_fontsize)

        g.add_legend(title = groupby, fontsize = label_fontsize-4, loc= 'upper left', bbox_to_anchor=(right_per*0.98, 0.75))
        plt.setp(g._legend.get_title(), fontsize= label_fontsize)
        g._legend._legend_box.align = "left"

        # plt.setp(g._legend.get_title(), fontsize = label_fontsize)
        # plt.setp(g._legend.get_texts(), fontsize = label_fontsize-4)
        # g._legend._legend_box.align = "left"
        # rectangles = {"N.S.  0.05 < p <= 1": matplotlib.patches.Patch(color='white'),
        #               "*       0.01 < p <= 0.05": matplotlib.patches.Patch(color='white'),
        #               "**     0.001 < p <= 0.01": matplotlib.patches.Patch(color='white'),
        #               "***    p <= 0.001": matplotlib.patches.Patch(color='white')}

        rectangles = {"0.05 < q <= 1": mlines.Line2D([], [], color='black',linewidth = 0, marker='$N.S.$',markersize=35),
                      "0.01 < q <= 0.05": mlines.Line2D([], [], color='black',linewidth = 0, marker='$*$',markersize=15),
                      "0.001 < q <= 0.01": mlines.Line2D([], [], color='black',linewidth = 0, marker='$**$',markersize=20),
                      "q <= 0.001": mlines.Line2D([], [], color='black',linewidth = 0, marker='$***$',markersize=40)}
        if len(legends) == 2:
            comp_pairs = list(zip(zip(annotation,[legends[0]]*len(annotation)),zip(annotation,[legends[1]]*len(annotation))))
            for i in range(len(genes)):
                add_stat_annotation(g.axes.ravel()[i], data=gene_df.loc[gene_df['Gene']==genes[i]], x=annotation_level, y='Expression',
                                    hue = groupby, order = annotation, hue_order = legends,
                                    box_pairs=comp_pairs, comparisons_correction = "bonferroni",line_draw = False,
                                    test='Mann-Whitney', text_format='star', loc='inside', verbose=0, fontsize = label_fontsize*0.9,
                                    pvalue_thresholds = [[1e-3, "***"], [1e-2, "**"], [0.05, "*"], [1, "N.S."]])

            legend = g.add_legend(legend_data = rectangles,
                         title = "Mann-Whitney U test", 
                         handlelength=2.5, handletextpad = 0.4, fontsize = label_fontsize-4, loc = 'lower left',bbox_to_anchor=(right_per*0.98, 0.25))

        if len(legends) > 2:
            comp_pairs = list(zip(zip(annotation,[legends[0]]*len(annotation)),zip(annotation,[legends[len(legends)-1]]*len(annotation))))
            for i in range(len(genes)):
                pvalues_list = []
                for j in range(len(annotation)):
                    df = gene_df.loc[(gene_df['Gene']==genes[i]) & (gene_df[annotation_level]==annotation[j])]
                    group_value_list = []
                    for m in range(len(legends)):
                        group_value_list.append(df.loc[df[groupby] == legends[m], "Expression"].tolist())
                    try:
                        stat, pvalue = stats.kruskal(*group_value_list)
                    except:
                        stat, pvalue = np.nan, np.nan
                    pvalues_list.append(pvalue)
                add_stat_annotation(g.axes.ravel()[i], data=gene_df.loc[gene_df['Gene']==genes[i]], x=annotation_level, y='Expression',
                                    hue = groupby, order = annotation, hue_order = legends, comparisons_correction = "bonferroni",
                                    box_pairs=comp_pairs, perform_stat_test = False,pvalues = pvalues_list,line_draw = False,
                                    text_format='star', loc='inside', verbose=0, fontsize = label_fontsize*0.9,
                                    pvalue_thresholds = [[1e-3, "***"], [1e-2, "**"], [0.05, "*"], [1, "N.S."]])
            legend = g.add_legend(legend_data = rectangles,
                         title = "Kruskal-Wallis test", 
                         handlelength=2.5, handletextpad = 0.4, fontsize = label_fontsize-4, loc = 'lower left',bbox_to_anchor=(right_per*0.98, 0.25))

        plt.setp(g._legend.get_title(), fontsize=label_fontsize)
        g._legend._legend_box.align = "left"

        g.fig.savefig(out_file, dpi = 200)
        plt.close(g.fig)
        plt.clf()
        plt.cla()
        # plt.clf()
        # plt.cla()
        # plt.close()
    out_file_return = out_file.split(BASE_DIR)[1]

    return out_file_return


def ViolinGridDatasetComparePlot(gene_df, dataset, comparison, groupby):
    DefaulfColorPalette = ["#E58606", "#5D69B1", "#52BCA3", "#99C945", "#CC61B0", "#24796C",
        "#DAA51B", "#2F8AC4", "#764E9F", "#ED645A", "#A5AA99", "#BCBD22",
        "#B279A2", "#EECA3B", "#17BECF", "#FF9DA6", "#778AAE", "#1B9E77",
        "#A6761D", "#526A83", "#B82E2E", "#80B1D3", "#68855C", "#D95F02",
        "#BEBADA", "#AF6458", "#D9AF6B", "#9C9C5E", "#625377", "#8C785D"]
    out_dir = os.path.join(BASE_DIR, "media/tmp/") + randomString()

    genes = sorted(list(set(gene_df["Gene"].tolist())))
    # if len(genes) == 6:
    #     height = 3
    #     aspect = 12
    #     label_fontsize = 38
    #     title_fontsize = 50
    #     top_per = 0.9
    # if len(genes) == 5:
    #     height = 4
    #     aspect = 10
    #     label_fontsize = 40
    #     title_fontsize = 55
    #     top_per = 0.9
    # if len(genes) == 4:
    #     height = 5
    #     aspect = 8
    #     label_fontsize = 40
    #     title_fontsize = 55
    #     top_per = 0.9
    # if len(genes) == 3:
    #     height = 6
    #     aspect = 7
    #     label_fontsize = 40
    #     title_fontsize = 55
    #     top_per = 0.9
    # if len(genes) == 2:
    #     height = 7
    #     aspect = 6
    #     label_fontsize = 40
    #     title_fontsize = 55
    #     top_per = 0.9
    # if len(genes) == 1:
    #     height = 6
    #     aspect = 5
    #     label_fontsize = 30
    #     title_fontsize = 35
    #     top_per = 0.85

    if len(genes) == 6:
        height = 2.6
        aspect = 12
        label_fontsize = 32
        title_fontsize = 38
        top_per = 0.9
    if len(genes) == 5:
        height = 2.8
        aspect = 10
        label_fontsize = 30
        title_fontsize = 35
        top_per = 0.9
    if len(genes) == 4:
        height = 3
        aspect = 8
        label_fontsize = 25
        title_fontsize = 30
        top_per = 0.9
    if len(genes) == 3:
        height = 4
        aspect = 7
        label_fontsize = 25
        title_fontsize = 30
        top_per = 0.9
    if len(genes) == 2:
        height = 6
        aspect = 6
        label_fontsize = 30
        title_fontsize = 35
        top_per = 0.9
    if len(genes) == 1:
        height = 9
        aspect = 5
        label_fontsize = 20
        title_fontsize = 22
        top_per = 0.85
    
    outfile_dict = {}
    out_file = "%s_%s_violin_multiple_%s_%s.png" %(out_dir, dataset, comparison, groupby)

    annotation = sorted(list(set(gene_df[comparison].tolist())))

    # ratio = 1.3 - 0.1*(len(celltypes)-1)
    # if 0.3 < ratio < 0.7:
    #     ratio = 0.7
    # if 0 < ratio <= 0.3:
    #     ratio = 0.5
    # if -0.4 < ratio <= 0:
    #     ratio = 0.5
    # if -0.7 < ratio <= -0.4:
    #     ratio = 0.4
    # if ratio <= -0.7:
    #     ratio = 0.35
    # aspect = len(celltypes)*ratio*3.5/height
    aspect = (len(annotation)*2.0/15 + 10.0/3)*len(genes)/3
    right_per = len(annotation)*0.1/16 + 0.775
    if len(annotation) <=4:
        aspect = 4*len(genes)/3
        right_per = 0.8
    if len(annotation) >= 20:
        aspect = 6*len(genes)/3
        right_per = 0.9


    sns.set(style="whitegrid", palette="Set2")
    g = sns.catplot(x=comparison, y='Expression', hue=groupby, data = gene_df,
                   row='Gene',  kind='violin', margin_titles=False, height = height, 
                   aspect = aspect, sharex = True, row_order = genes,
                   order = annotation, scale="width", cut=0, linewidth = 1.2)
    g.set_titles(row_template = '')
    g.set_xlabels(label = '')
    for i in range(len(genes)):
        ax = g.axes.flatten()[i]
        ax.set_ylabel(ylabel = genes[i], fontsize = label_fontsize, rotation = "horizontal", horizontalalignment = "right", verticalalignment = "center")
        for label in ax.get_xticklabels():
            label.set_rotation(315)
            label.set_horizontalalignment("left")
            label.set_fontsize(label_fontsize)
            
    g.fig.tight_layout()
    g.fig.subplots_adjust(top = top_per, right = right_per)
    g.fig.suptitle(dataset, fontsize = title_fontsize)
    plt.setp(g._legend.get_title(), fontsize = label_fontsize)
    plt.setp(g._legend.get_texts(), fontsize = label_fontsize-4)
    g._legend._legend_box.align = "left"
    g.savefig(out_file, dpi = 200)
    plt.close(g.fig)
    plt.clf()
    plt.cla()

    out_file_return = out_file.split(BASE_DIR)[1]

    return out_file_return


def GenerateDotplotData(dataset, gene_list):

    pct_file = os.path.join(BASE_DIR, "static/data/%s/%s_percent_curated.txt" %(dataset,dataset))
    expr_file = os.path.join(BASE_DIR, "static/data/%s/%s_expression_Celltype_curated.txt" %(dataset, dataset))
    pct_df = pd.read_csv(pct_file, sep = "\t")
    expr_df = pd.read_csv(expr_file, sep = "\t")

    gene_overlap = list(set(gene_list) & set(pct_df.index))
    # gene_overlap.sort()

    df_columns = list(pct_df.columns)
    df_columns.sort()
    pct_gene_df = pct_df.loc[gene_overlap, df_columns]
    pct_gene_df = pct_gene_df.sort_index(ascending = False)
    expr_gene_df = expr_df.loc[gene_overlap, df_columns]
    expr_gene_df = expr_gene_df.sort_index(ascending = False)

    pct_gene_df = pct_gene_df*100

    gene_rep = [];
    for i in expr_gene_df.index.to_list():
        gene_rep0 = [i]*expr_gene_df.shape[1]
        gene_rep = gene_rep + gene_rep0

    gene_celltype_dict = {"expression": expr_gene_df.values.flatten().tolist(), "percent": pct_gene_df.values.flatten().tolist(), 
    "celltype": expr_gene_df.columns.to_list()*expr_gene_df.shape[0], "gene": gene_rep, "genenumber": expr_gene_df.shape[0]}

    out_dir = os.path.join(BASE_DIR, "media/tmp/") + randomString()
    dotplot_file = "%s_%s_dotplot.json" %(out_dir, dataset)
    json.dump(gene_celltype_dict, open(dotplot_file, "w"))

    out_file_return = dotplot_file.split(BASE_DIR)[1]
    return out_file_return

def GenerateForm(dataset):
    umap_file = os.path.join(BASE_DIR, "static/data/%s/%s_umap.json" %(dataset, dataset))
    umap_dict = json.load(open(umap_file, "r"))
    available_annotation_list = list(set(umap_dict.keys()) - {'Cell', 'UMAP_1', 'UMAP_2'})
    available_meta = list(set(umap_dict.keys()) - {'Cell', 'UMAP_1', 'UMAP_2', 'Celltype_curated', 'Celltype_general', 'Celltype_subtype', 'Celltype_paper', 'Cluster'})
    available_meta.sort()
    if "Celltype_paper" in available_annotation_list:
        available_annotation = ["Celltype_general", "Celltype_curated", "Celltype_subtype", "Celltype_paper", "Cluster"]
        available_annotation_name = ["Celltype (malignancy)", "Celltype (major-lineage)", "Celltype (minor-lineage)", "Celltype (original)", "Cluster"]
    else:
        available_annotation = ["Celltype_general", "Celltype_curated", "Celltype_subtype", "Cluster"]
        available_annotation_name = ["Celltype (malignancy)", "Celltype (major-lineage)", "Celltype (minor-lineage)", "Cluster"]


    # available_annotation_name = available_annotation.copy()
    # available_annotation_name[available_annotation_name.index("Celltype_curated")] = "Celltype (major-lineage)"
    # available_annotation_name[available_annotation_name.index("Celltype_general")] = "Celltype (malignancy)"
    # available_annotation_name[available_annotation_name.index("Celltype_subtype")] = "Celltype (minor-lineage)"
    # if "Celltype_paper" in available_annotation_name:
    #     available_annotation_name[available_annotation_name.index("Celltype_paper")] = "Celltype (paper)"
    cluster_choices = []
    cluster_choices.append(("All cells", "All cells"))
    annotation_choices = list(zip(available_annotation, available_annotation_name))
    available_annotation = available_annotation + available_meta
    available_annotation_name = available_annotation_name + available_meta
    annotation_choices_all = list(zip(available_annotation, available_annotation_name))
    meta_chices = list(zip(available_meta, available_meta))

    # for annotation in available_annotation:
    #     unique_cluster = sorted(list(set(umap_dict[annotation])))
    #     unique_cluster_zip = tuple(zip(unique_cluster, unique_cluster))
    #     cluster_choices.append((annotation, unique_cluster_zip))
    # class LoadClusterForm(forms.Form):
    #     cluster = forms.ChoiceField(choices=cluster_choices, widget=forms.Select(attrs={'class': 'form-control', 'name':'loadcluster', 'id': 'loadcluster'}))

    class AnnotationForm(forms.Form):
        annotation = forms.ChoiceField(choices=annotation_choices_all, widget=forms.Select(attrs={'class': 'form-control', 'name':'annotation', 'id': 'annotation'})) 

    class ComparisonForm(forms.Form):
        comparison = forms.ChoiceField(choices=annotation_choices, widget=forms.Select(attrs={'class': 'form-control', 'name':'comparison', 'id': 'comparison'})) 

    class GroupForm(forms.Form):
        group = forms.ChoiceField(choices=[("None", "None")] + meta_chices, widget=forms.Select(attrs={'class': 'form-control', 'name':'group', 'id': 'group'})) 

    # cluster_form = LoadClusterForm().as_p().split("</label>")[1].split("</p>")[0]
    annotation_form = AnnotationForm().as_p().split("</label>")[1].split("</p>")[0]
    comparison_form = ComparisonForm().as_p().split("</label>")[1].split("</p>")[0]
    group_form = GroupForm().as_p().split("</label>")[1].split("</p>")[0]
    return {'annotation_form': annotation_form, 'comparison_form':comparison_form, 'group_form':group_form}


def GenerateDiffgeneTable(dataset):
    diff_gene_file = os.path.join(BASE_DIR, "static/data/%s/%s_AllDiffGenes.tsv" %(dataset, dataset))
    umap_file = os.path.join(BASE_DIR, "static/data/%s/%s_umap.json" %(dataset, dataset))
    umap_dict = json.load(open(umap_file, "r"))
    umap_df = pd.DataFrame(umap_dict)
    cluster_annotation_df = umap_df[["Cluster", "Celltype_general", "Celltype_curated", "Celltype_subtype"]]
    cluster_annotation_df = cluster_annotation_df.drop_duplicates()
    cluster_annotation_df["Cluster"] = [int(i) for i in cluster_annotation_df["Cluster"]]

    diff_gene_df = pd.read_csv(diff_gene_file, sep = "\t")
    diff_gene_df = diff_gene_df.merge(cluster_annotation_df, left_on='cluster', right_on='Cluster')
    diff_gene_df = diff_gene_df.iloc[:,[7, 8, 9, 10, 6, 1, 2, 4]]
    diff_gene_df["avg_logFC"] = diff_gene_df["avg_logFC"].round(2)
    diff_gene_df["pct.1"] = diff_gene_df["pct.1"].round(2)
    diff_gene_df["p_val_adj"] = diff_gene_df["p_val_adj"].map(lambda x: "%.3g" % x)
    diff_gene_list = diff_gene_df.values.tolist()

    return diff_gene_list[:20]

def GenerateDotplotCPDBData(dataset, gene_pairs_rank, cell_list):

    ##read in cpdb result
    interaction_file = os.path.join(BASE_DIR, "static/data/%s/CPDB/significant_means.txt" % (dataset))
    pvalue_file = os.path.join(BASE_DIR, "static/data/%s/CPDB/pvalues.txt" % (dataset))
    mean_file = os.path.join(BASE_DIR, "static/data/%s/CPDB/means.txt" % (dataset))
    interaction_df = pd.read_csv(interaction_file, sep = "\t")
    pvalue_df = pd.read_csv(pvalue_file, sep = "\t")
    mean_df = pd.read_csv(mean_file, sep = "\t")

    ##get all cell-cell pairs based on selected cell_list
    cell_pair_list = [cell1+"|"+cell2 for cell1 in cell_list for cell2 in cell_list]
    cell_pair_list.sort()

    ## get gene_pairs based on the selected gene_pairs_rank
    interaction_df["rank"] = interaction_df["rank"] 
    interaction_df_sub = interaction_df.loc[interaction_df["rank"] < gene_pairs_rank]
    interaction_df_sub = interaction_df_sub[interaction_df_sub.columns.intersection(["interacting_pair"] + cell_pair_list)]

    ## filtering out gene pairs which are not significant in all cell pairs
    gene_na_count = interaction_df_sub.isnull().sum(axis=1).tolist()
    non_na_index = [i for i,x in enumerate(gene_na_count) if x != interaction_df_sub.shape[1]-1]
    interaction_df_sub = interaction_df_sub.iloc[non_na_index]
    gene_pairs_list = interaction_df_sub["interacting_pair"].tolist()
    gene_pairs_list.sort(reverse = True)
    # print(len(gene_pairs_list))
    # print(interaction_df_sub["rank"].tolist())

    ## sub means_df on gene_pairs and cell_pair_list
    mean_df.index = mean_df["interacting_pair"].tolist()
    mean_df_sub = mean_df[mean_df.columns.intersection(cell_pair_list)]
    mean_df_sub = mean_df_sub.loc[gene_pairs_list]
    mean_df_sub = mean_df_sub.replace(0,1)
    mean_df_sub = np.log2(mean_df_sub)
    # print(mean_df_sub.columns)

    ## sub means_df on gene_pairs and cell_pair_list
    pvalue_df.index = pvalue_df["interacting_pair"].tolist()
    pvalue_df_sub = pvalue_df[pvalue_df.columns.intersection(cell_pair_list)]
    pvalue_df_sub = pvalue_df_sub.loc[gene_pairs_list]
    pvalue_df_sub = pvalue_df_sub.replace(0,0.0009)
    pvalue_df_sub = np.log10(1/pvalue_df_sub) 
    # print(pvalue_df_sub)

    # ##generate dict
    gene_cell_pairs_dict = {"means": mean_df_sub.values.flatten().tolist(),
                            "pvalue": pvalue_df_sub.values.flatten().tolist(),
                            "cell_pairs": list(mean_df_sub.columns),  #*mean_df_sub.shape[0]
                            "gene_pairs": gene_pairs_list} #*mean_df_sub.shape[1]
    # print(gene_cell_pairs_dict)
    print(len(mean_df_sub.values.flatten().tolist()))
    print(len(list(mean_df_sub.columns)*mean_df_sub.shape[0]))
    print(len(gene_pairs_list*mean_df_sub.shape[1]))
    ##write json file

    out_dir = os.path.join(BASE_DIR, "media/tmp/") + randomString()
    cpdb_dotplot_file = "%s_%s_cpdb_dotplot.json" %(out_dir, dataset)
    json.dump(gene_cell_pairs_dict, open(cpdb_dotplot_file, "w"))

    out_file_return = cpdb_dotplot_file.split(BASE_DIR)[1]
    return out_file_return
