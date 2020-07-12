library(Seurat)
library(rjson)

setwd("/home1/wangchenfei/Project/TIRA/scTumor_Data")

PercentAbove <- function(x, threshold) {
  return(length(x = x[x > threshold]) / length(x = x))
}

AverageExpressionMAESTRO <- function(RNA){
  cluster_cell_list = split(names(Idents(RNA)), Idents(RNA))
  expr = GetAssayData(object = RNA, assay="RNA", slot = "data")
  
  # # if expm1, the result will be equal to AverageExpression
  # expr = expm1(GetAssayData(object = RNA, assay="RNA", slot = "data"))
  cluster_avg_expr <- sapply(names(cluster_cell_list), function(x){
    return(Matrix::rowMeans(expr[, cluster_cell_list[[x]]]))
  })
}


dirs = c("PBMC_60K_10X", "PBMC_30K_10X", "PBMC_8K_10X")
dirs = c("BLCA_GSE145281_aPD1", "MM_GSE141299", "KIRC_GSE145281_aPD1")
for (dir in dirs) {
  objects = list.files(dir, "_res.rds")
  if (length(which(grepl("CCA", objects))) > 0){
    objects = objects[grepl("CCA", objects)]
  }
  for (i in objects){
    SeuratObj = readRDS(file.path(dir,i))
    
    project.name = gsub("_CCA","", SeuratObj$RNA@project.name)

    # umap info
    umap.df = as.data.frame(SeuratObj$RNA@reductions$umap@cell.embeddings)
    umap.df$Celltype_general = as.character(SeuratObj$RNA@meta.data$assign.level1_anno)
    umap.df$Celltype_curated = as.character(SeuratObj$RNA@meta.data$assign.curated)
    umap.df$Celltype_subtype = as.character(SeuratObj$RNA@meta.data$assign.level3_anno)

    umap.df$Cell = rownames(umap.df)
    umap.df = umap.df[order(umap.df$Celltype_curated),c(6,1:5)]
    # umap.list = as.list(umap.df)
    # umap_json = file.path(dir, paste0(project.name, "_umap.json"))
    # write(toJSON(umap.list), umap_json)
    
    # average expression
    Idents(object = SeuratObj$RNA) <- 'assign.curated'
    RNA.mean = AverageExpressionMAESTRO(SeuratObj$RNA)
    RNA.mean = round(RNA.mean, 5)
    expr_file = file.path(dir, paste0(project.name, "_expression_Celltype_majorlineage.txt"))
    write.table(RNA.mean, expr_file, sep="\t", quote=F)
    
    Idents(object = SeuratObj$RNA) <- 'assign.level1_anno'
    RNA.mean = AverageExpressionMAESTRO(SeuratObj$RNA)
    RNA.mean = round(RNA.mean, 5)
    expr_file = file.path(dir, paste0(project.name, "_expression_Celltype_malignancy.txt"))
    write.table(RNA.mean, expr_file, sep="\t", quote=F)
    
    Idents(object = SeuratObj$RNA) <- 'assign.level3_anno'
    RNA.mean = AverageExpressionMAESTRO(SeuratObj$RNA)
    RNA.mean = round(RNA.mean, 5)
    expr_file = file.path(dir, paste0(project.name, "_expression_Celltype_minorlineage.txt"))
    write.table(RNA.mean, expr_file, sep="\t", quote=F)

    Idents(object = SeuratObj$RNA) <- 'seurat_clusters'
    RNA.mean = AverageExpressionMAESTRO(SeuratObj$RNA)
    RNA.mean = round(RNA.mean, 5)
    expr_file = file.path(dir, paste0(project.name, "_expression_Cluster.txt"))
    write.table(RNA.mean, expr_file, sep="\t", quote=F)
    
    # expression matrix
    matrix <- GetAssayData(object = SeuratObj$RNA, slot = "data", assay = "RNA")
    matrix = matrix[,umap.df$Cell]
    mtx_file = file.path(dir, paste0(project.name, "_matrix.mtx"))
    gene_file = file.path(dir, paste0(project.name, "_genes.tsv"))
    barcode_file = file.path(dir, paste0(project.name, "_barcodes.tsv"))
    Matrix::writeMM(matrix, mtx_file)
    write.table(rownames(matrix), gene_file, col.names = FALSE, row.names = FALSE, quote = FALSE)
    write.table(colnames(matrix), barcode_file, col.names = FALSE, row.names = F, quote = FALSE)

    # expression matrix to h5
    cmd = paste0("MAESTRO mtx-to-h5 --type Gene --matrix ", mtx_file,
                 " --feature ", gene_file, " --gene-column 1 --barcode ", barcode_file,
                 " --species GRCh38 --directory " ,dir, " --outprefix ", project.name)
    system(cmd)

    # # percentage of expressed genes
    # Idents(object = SeuratObj$RNA) <- 'assign.curated'
    # cluster_cell_list = split(colnames(SeuratObj$RNA), SeuratObj$RNA[["assign.curated"]])
    # cluster_gene_pct <- sapply(names(cluster_cell_list), function(x){
    #   gene_mat = GetAssayData(object = SeuratObj$RNA, slot = "data", assay = "RNA")[, cluster_cell_list[[x]]]
    #   pct.exp <- apply(X = gene_mat, MARGIN = 1, FUN = PercentAbove, threshold = 0)
    # })
    # pct_file = file.path(dir, paste0(project.name, "_percent_curated.txt"))
    # write.table(cluster_gene_pct, pct_file, sep="\t", quote=F)
    
    message(i)
  }
}

