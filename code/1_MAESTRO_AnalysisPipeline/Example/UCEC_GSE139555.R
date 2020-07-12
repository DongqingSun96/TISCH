# load package
library(MAESTRO)
library(Seurat)
library(ggplot2)
library(future)
plan("multiprocess", workers = 8)
options(future.globals.maxSize = 10*1024^3)

# read data
expr = Read10X_h5("/home1/wangchenfei/Project/TIRA/Data_cancer_new/LECR_GSE139555/Data/LECR_GSE139555_UCEC_filtered_gene_count.h5")

# clustering
RNA.res = RNARunSeurat(inputMat = expr, 
                       project = "UCEC_GSE139555", 
                       min.c = 10,
                       min.g = 500,
                       dims.use = 1:30,
                       variable.genes = 2000, 
                       organism = "GRCh38",
                       cluster.res = 1,
                       genes.test.use = "presto",
                       only.pos = TRUE,
                       genes.cutoff = 1e-05)

# cell-type annotation
RNA.res$RNA = RNAAnnotateCelltype(RNA = RNA.res$RNA, 
                                  genes = RNA.res$genes,
                                  signatures = "human.immune.CIBERSORT",
                                  min.score = 0.6)

# add metadata
meta = read.delim("/home1/wangchenfei/Project/TIRA/Data_cancer_new/LECR_GSE139555/Data/LECR_GSE139555_meta.txt", header = T, row.names = 1, sep = "\t")
RNA.res$RNA@meta.data = cbind(RNA.res$RNA@meta.data, meta[colnames(RNA.res$RNA),, drop = FALSE])
for (i in colnames(meta)) {
  p = DimPlot(object = RNA.res$RNA, group = i, label = FALSE, pt.size = 0.1)
  if (length(unique(RNA.res$RNA@meta.data[,i])) > 20) {
    plot_width = 10
  } else {
    plot_width = 7
  }
  ggsave(file.path(paste0(RNA.res$RNA@project.name, "_", i, ".png")), p,  width=plot_width, height=5)
}

# save object
saveRDS(RNA.res, "UCEC_GSE139555_res.rds")

{
  # check batch effect
  RNA.res = readRDS("UCEC_GSE139555_res.rds")
 
  p = DimPlot(object = RNA.res$RNA, group = "source", label = TRUE, pt.size = 0.1)
  ggsave(file.path(paste0(RNA.res$RNA@project.name, "_", "source", ".png")), p,  width=6.5, height=5)
  p = DimPlot(object = RNA.res$RNA, group = "patient", label = TRUE, pt.size = 0.1)
  ggsave(file.path(paste0(RNA.res$RNA@project.name, "_", "patient", ".png")), p,  width=6.5, height=5)
  p = DimPlot(object = RNA.res$RNA, group = "sample", label = TRUE, pt.size = 0.1)
  ggsave(file.path(paste0(RNA.res$RNA@project.name, "_", "sample", ".png")), p,  width=6.5, height=5)
}

{
  # remove batch effect
  RNA.res = readRDS("UCEC_GSE139555_res.rds")
  
  RNA.res <- RNABatchCorrect(RNA.res$RNA, RNA.res$RNA@meta.data$patient, 
                             nfeatures = 3000, dims.use = 1:30, cluster.res = 1, only.pos = TRUE, 
                             runpca.agrs = list(npcs = 50))
  p = DimPlot(object = RNA.res$RNA, group = "patient", label = TRUE, pt.size = 0.1)
  ggsave(file.path(paste0(RNA.res$RNA@project.name, "_", "patient", ".png")), p,  width=6.5, height=5)
  
  p = DimPlot(object = RNA.res$RNA, group = "source", label = TRUE, pt.size = 0.1)
  ggsave(file.path(paste0(RNA.res$RNA@project.name, "_", "source", ".png")), p,  width=6.5, height=5)

  p = DimPlot(object = RNA.res$RNA, group = "sample", label = TRUE, pt.size = 0.1)
  ggsave(file.path(paste0(RNA.res$RNA@project.name, "_", "sample", ".png")), p,  width=6.5, height=5)
  
  # cell-type annotation
  RNA.res$RNA = RNAAnnotateCelltype(RNA = RNA.res$RNA, 
                                    genes = RNA.res$genes,
                                    signatures = "human.immune.CIBERSORT",
                                    min.score = 0.3)
  saveRDS(RNA.res, "UCEC_GSE139555_CCA_res.rds")
}

{
  # check immunity
  RNA.res = readRDS("UCEC_GSE139555_CCA_res.rds")
  
  DefaultAssay(RNA.res$RNA) = "RNA"
  VisualizeUmap(SeuratObj = RNA.res$RNA, type = "RNA", genes = c("PTPRC", "CD8A", "CD8B", "CD3D"), ncol = 4,
                width = 20, height = 4, name = paste0(RNA.res$RNA@project.name, "_immunity"))
}

{
  # curated cell-type annotation
  
  # CD8Tex: HAVCR2, LAG3, PDCD1
  
  RNA.res = readRDS("UCEC_GSE139555_CCA_res.rds")
  
  DefaultAssay(RNA.res$RNA) = "RNA"
  VisualizeUmap(SeuratObj = RNA.res$RNA, type = "RNA", genes = c("HAVCR2", "LAG3", "PDCD1"), ncol = 3,
                width = 15, height = 4, name = paste0(RNA.res$RNA@project.name, "_CD8Tex"))
  
  DefaultAssay(RNA.res$RNA) = "integrated"
  RNA.res$RNA@meta.data$assign.CIBERSORT = RNA.res$RNA@meta.data$assign.ident
  RNA.res$RNA@meta.data$assign.curated = as.character((RNA.res$RNA$seurat_clusters))
  current.cluster.ids = as.character(0:(length(unique(RNA.res$RNA@meta.data$assign.curated))-1))
  new.cluster.ids = c("CD8T","CD4Tconv","CD4Tconv","CD8T",
                      "Treg","CD8Tex","CD8T","CD4Tconv",
                      "CD4Tconv","CD4Tconv","Treg","CD8Tex",
                      "TMKI67","Fibroblasts")
  RNA.res$RNA@meta.data$assign.curated = plyr::mapvalues(x = RNA.res$RNA@meta.data$assign.curated,
                                                         from = current.cluster.ids, to = new.cluster.ids)
  
  p = DimPlot(object = RNA.res$RNA, group = "assign.CIBERSORT", label = TRUE, pt.size = 0.1)
  ggsave(file.path(paste0(RNA.res$RNA@project.name, "_", "annotated_CIBERSORT", ".png")), p,  width=7, height=5)
  p = DimPlot(object = RNA.res$RNA, group = "assign.curated", label = TRUE, pt.size = 0.1)
  ggsave(file.path(paste0(RNA.res$RNA@project.name, "_", "annotated_curated", ".png")), p,  width=7, height=5)
  
  saveRDS(RNA.res, "UCEC_GSE139555_CCA_res.rds")
}

{
  # generate umap json file (UMAP info, clustering, annotation, meta info)
  RNA.res = readRDS("UCEC_GSE139555_CCA_res.rds")
  dim(RNA.res$RNA)
  head(RNA.res$RNA@meta.data)

  umap.df = as.data.frame(RNA.res$RNA@reductions$umap@cell.embeddings)
  meta.col = c("seurat_clusters", "assign.level1_anno", "assign.curated", "assign.level3_anno", "patient", "sample", "source")
  meta.df = RNA.res$RNA@meta.data[,meta.col]
  colnames(meta.df) = c("Cluster", "Celltype_general", "Celltype_curated", "Celltype_subtype", "Patient", "Sample", "Tissue")
  for (i in 1:length(meta.col)) {
    meta.df[,i] = as.character(meta.df[,i])
  }
  
  umap.df = cbind(umap.df, meta.df)
  umap.df$Cell = rownames(umap.df)

  umap.df = umap.df[order(umap.df$Celltype_curated),]
  umap.df = umap.df[,c(ncol(umap.df), 1:(ncol(umap.df)-1))]
  umap.list = as.list(umap.df)

  project.name = gsub("_CCA","", RNA.res$RNA@project.name)
  umap_json = file.path(paste0(project.name, "_umap.json"))
  # umap_json = file.path(paste0(project.name, "_umap.json"))
  write(toJSON(umap.list), umap_json)

  # DE analysis (positive and negative)
  diff.gene.all = FindAllMarkersMAESTRO(object = RNA.res$RNA, test.use = "presto", min.pct = 0.1, logfc.threshold = 0.25, only.pos = FALSE)
  diff.gene.all <- diff.gene.all[diff.gene.all$p_val_adj<1e-05, ]
  write.table(diff.gene.all, paste0(project.name, "_AllDiffGenes.tsv"), quote = F, sep = "\t")
}

