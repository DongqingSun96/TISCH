library(Seurat)
library(jsonlite)
library(dplyr)
library(stringr)
library(utils)
library(optparse)
library(future)
plan("multiprocess", workers = 8)
options(future.globals.maxSize = 10*1024^3)

option_list <- list(  
  make_option(c("-i", "--input"), type="character", 
              help="Input file of seurat object"),
  make_option(c("-o", "--output"), type="character",
              help="Ouput path of count data and meta data. [Required]"),
  make_option(c("-j", "--json"), type="character", 
              help="json file"),
  make_option(c("-m", "--meta"), type="character",
              help="meta file")
)
opt_parser <- OptionParser(option_list=option_list,add_help_option = FALSE);
opts <- parse_args(opt_parser);

input <- opts$input
output <- opts$output
json_file <- opts$json
meta <- opts$meta


### read in seurat object
RNA.res <- readRDS(input)
name <- gsub("_CCA","", RNA.res$RNA@project.name)

### save result recording cluster and corresponding cell type
cluster_cell <- data.frame(cluster=as.character(RNA.res$RNA@meta.data$seurat_clusters),
                           cell_level1=as.character(RNA.res$RNA@meta.data$assign.level1_anno),
                           cell_level2=as.character(RNA.res$RNA@meta.data$assign.curated),
                           cell_level3=as.character(RNA.res$RNA@meta.data$assign.level3_anno),
                           cell_maestro=as.character(RNA.res$RNA@meta.data$assign.CIBERSORT))
cluster_cell_uiq <- cluster_cell[!duplicated(cluster_cell),]
write.table(cluster_cell_uiq,paste(output, name, "_cluster_cell.txt", sep = ""), quote = FALSE, sep = "\t", row.names = FALSE)

#### extract the specific meta column in the rds file
json <- fromJSON(json_file, flatten=TRUE)
json <- as.data.frame(json)
json.df <- subset(json, select=colnames(json)[! colnames(json) %in% c("UMAP_1","UMAP_2","Cluster", "Celltype_general", "Celltype_curated", "Celltype_subtype")])
uniq_val <- sort(unique(as.character(json.df[,meta])))
map_col <- unlist(lapply(colnames(RNA.res$RNA@meta.data), function(col){
    ori_val <- sort(unique(as.character(RNA.res$RNA@meta.data[,col])))
    ori_val <- ori_val[ori_val != "NA"]
    if(setequal(uniq_val, ori_val)){return(col)}
}))
print(paste("The corresponding meta column of ",meta," in rds is ",map_col ,sep = ""))


### create a new identity for recording cluster and conditions
conditions <- gsub(" ","",(gsub("/","|",gsub("-","",RNA.res$RNA[[map_col]][,1])))) # remove specific character in meta condition
RNA.res$RNA$cluster.condition <- paste(Idents(RNA.res$RNA), conditions, sep = "_")
Idents(RNA.res$RNA) <- "cluster.condition"

### extract all combinations for different conditions in each cluster (make sure each condition has >3 cells in each cluster)
cd_cell <- table(RNA.res$RNA$cluster.condition)[table(RNA.res$RNA$cluster.condition) >= 3]
cluster <- data.frame(do.call("rbind",strsplit(names(cd_cell), "\\_")))
colnames(cluster) <- c("cl","cd")
cluster_df <- cluster %>% group_by(cl) %>% summarise(conts = paste(cd, collapse = ",")) %>% mutate(n = str_count(conts,",")+1) %>% filter(n > 1)
print(cluster_df)

for(c in cluster_df$cl){
    cds <- unlist(subset(cluster_df, cl == c, select = "conts"))
    cds <- strsplit(cds, ",")[[1]]
    comb <- combn(cds,2)
    print(c)
    for(gr in 1:ncol(comb)){
        compare <- c(comb[1,gr], comb[2,gr])
        compare <- sort(compare, decreasing = TRUE)
        c1 <- paste(c, compare[1], sep = "_")
        c2 <- paste(c, compare[2], sep = "_")
        print(paste("perform differential analysis on ", c1," VS ", c2, " in cluster ", c,sep = ""))
        condition.cluster.genes <- FindMarkersMAESTRO(RNA.res$RNA, ident.1 = c1, ident.2 = c2, verbose = FALSE, 
                                               min.pct = 0.1, min.cells.group = 3, logfc.threshold = 0, slot = "data", only.pos = FALSE)
        condition.cluster.genes$gene <- rownames(condition.cluster.genes)
        print(dim(condition.cluster.genes))
        write.table(condition.cluster.genes, paste(output, name, "_",meta,"_C",c,"_",compare[1],"VS",compare[2],"_DE.txt",sep = ""), quote = FALSE, row.names = FALSE, sep = "\t")
    }
}
