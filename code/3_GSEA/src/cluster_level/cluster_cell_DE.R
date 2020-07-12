library(MAESTRO)
library(dplyr)
library(optparse)

option_list <- list(  
  make_option(c("-i", "--input"), type="character", 
              help="Input file of seurat object"),
  make_option(c("-o", "--output"), type="character",
              help="Ouput path of count data and meta data. [Required]")
)
opt_parser <- OptionParser(option_list=option_list,add_help_option = FALSE);
opts <- parse_args(opt_parser);

input <- opts$input
output <- opts$output

### read in rds file
rds <- readRDS(input)
name <- gsub("_CCA","", rds$RNA@project.name)

##do DE analysis in cluster level for PreRanked GSEA
cluster.genes <- FindAllMarkersMAESTRO(object = rds$RNA, min.pct = 0.1, logfc.threshold = 0, test.use = "presto", only.pos = FALSE)
write.table(cluster.genes,paste(output, name, "_cluster_DE.txt",sep = ""), quote = FALSE, sep = "\t")

### save result recording cluster and corresponding cell type
cluster_cell <- data.frame(cluster=as.character(rds$RNA@meta.data$seurat_clusters),
                           cell_level1=as.character(rds$RNA@meta.data$assign.level1_anno),
                           cell_level2=as.character(rds$RNA@meta.data$assign.curated),
                           cell_level3=as.character(rds$RNA@meta.data$assign.level3_anno),
                           cell_maestro=as.character(rds$RNA@meta.data$assign.ident))
cluster_cell_uiq <- cluster_cell[!duplicated(cluster_cell),]
write.table(cluster_cell_uiq,paste(output, name, "_cluster_cell.txt", sep = ""), quote = FALSE, sep = "\t", row.names = FALSE)

