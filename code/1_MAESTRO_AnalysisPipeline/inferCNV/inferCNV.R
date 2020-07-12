library("infercnv")
library(Seurat)
#Running InferCNV
##Creating an InferCNV object based on your three required inputs: the read count matrix, cell type annotations, and the gene ordering file:
setwd("/mnt/Storage2/home/wangjin/scTumor_Data/MM_GSE141299/Data/Infercnv_result")

###10x raw counts matrix
#SeuratObj <- readRDS("/mnt/Storage2/home/wangjin/scTumor_Data/MM_GSE141299/MM_GSE141299_res.rds")   #10x 
infercnv_obj = CreateInfercnvObject(raw_counts_matrix= "MM_GSE141299_10x.txt",
                                    annotations_file= "cell.anno.txt",
                                    delim="\t",
                                    gene_order_file= "inferCNV_gene_order_file.txt",
                                    ref_group_names=NULL)

# perform infercnv operations to reveal cnv signal
infercnv_obj = infercnv::run(infercnv_obj,
                             cutoff=0.1,  # use 1 for smart-seq/Fluidigm C1, 0.1 for 10x-genomics/SNRS/MARS-Seq/Microwell/Drop-seq
                             out_dir="k2.c1",  # dir is auto-created for storing outputs
                             cluster_by_groups=FALSE,   # cluster
                             k_obs_groups = 2,
                             denoise=T)