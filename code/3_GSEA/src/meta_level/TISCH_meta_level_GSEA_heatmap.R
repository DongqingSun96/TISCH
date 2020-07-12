library(ComplexHeatmap)
library(circlize)
library(dplyr)
library(reshape2)
library(RColorBrewer)

setwd("~/Documents/TISCH/GSEA_meta_cluster_all/")
outpath <- "../GSEA_meta_cluster_all_figures/"

### set cell colors
DefaulfColorPalette <- c(
  "#E58606", "#5D69B1", "#52BCA3", "#99C945", "#CC61B0", "#24796C",
  "#DAA51B", "#2F8AC4", "#764E9F", "#ED645A", "#A5AA99", "#BCBD22",
  "#B279A2", "#EECA3B", "#17BECF", "#FF9DA6", "#778AAE", "#1B9E77",
  "#A6761D", "#526A83", "#B82E2E", "#80B1D3", "#68855C", "#D95F02",
  "#BEBADA", "#AF6458", "#D9AF6B", "#9C9C5E", "#625377", "#8C785D"
)

### set pathway category colors
CatPlatte <- c(brewer.pal(name = "Set1", n = 9),
               brewer.pal(name = "Set2", n = 8),
               brewer.pal(name = "Set3", n = 12),
               brewer.pal(name = "Dark2", n = 8),
               brewer.pal(name = "Pastel1", n = 9))

###read in hallmark pathway category
hallmark_cat <- read.table("../src/MsigDB_Hallmark_Category", header = TRUE, row.names = 1)

###read in kegg pathway category
kegg_cat <- read.table("../src/MsigDB_KEGG_Category.txt", sep = "\t",  header = TRUE, row.names = 1)

###get all study folder
gsea_folders <- dir()

###perform hallmark and kegg analysis for all studies
for(ff in gsea_folders){
  print(ff)
  # ff <- "BLCA_GSE145281_Treatment_DE_GSEA"
  for(type in c("kegg","hallmark")){
    print(type)
    if(type == "kegg"){
      path_cat <- kegg_cat
    } else{
      path_cat <- hallmark_cat
    }
    meta <- gsub(".*GSE[0-9]+_(.*)_DE_GSEA","\\1",ff)
    PlotGSEA(folder = ff, type = type, outpath = outpath)
  }
}



### function of merging all gsea reports 
merge_gsea_reports <- function(gsea_dir){
  gsea_res <- lapply(gsea_dir, function(ff){
    mt <- strsplit(strsplit(ff,"\\/")[[1]][3],"\\_")[[1]][1]
    cl <- strsplit(strsplit(ff,"\\/")[[1]][3],"\\_")[[1]][2]
    comp <- gsub("VS"," VS ",strsplit(strsplit(ff,"\\/")[[1]][3],"\\_")[[1]][3])
    cond <- gsub("\\.","",gsub("treatment","",paste(comp, cl, sep = "_"))) 
    dirction <- gsub(".*na_(.*)_[0-9]+.*","\\1",ff)
    tryCatch({
      file <- read.table(ff, sep = "\t", header = TRUE)
      file.tmp <- subset(file, select = c("NAME","NES","FDR.q.val")) %>% mutate(direction = dirction) %>%
        mutate(meta = mt) %>%
        mutate(condition = cond) %>% 
        filter(FDR.q.val <= 0.05) %>% mutate(logFDR = -log10(FDR.q.val))
      return(file.tmp)
    },error = function(e) {cat("ERROR:",conditionMessage(e),"\n")})
  })
  gsea_res_all <- do.call("rbind", gsea_res)
  return(gsea_res_all)
}

### function of spliting all reports into a list containing up-regulated and down-regulated pathways
split_gsea_direction <- function(gsea_res){
  gsea_res_list <- list()
  for (i in c("pos","neg")){
    gsea_sub <- subset(gsea_res, direction == i)
    gsea_res_mat <- reshape2::dcast(gsea_sub, NAME~condition, value.var = "logFDR")
    rownames(gsea_res_mat) <- ifelse(grepl("KEGG",gsea_res_mat$NAME),gsub("KEGG_","",gsea_res_mat$NAME), gsub("HALLMARK_","",gsea_res_mat$NAME))
    gsea_res_mat <- gsea_res_mat[,-1]
    gsea_res_mat[is.na(gsea_res_mat)] <- 0
    total.num <- nrow(gsea_res_mat)*ncol(gsea_res_mat)
    if(length(which(gsea_res_mat == "Inf")) == total.num){  ### Inf refer to FDR as 0, when all logFDR values equal to 0, set them a big logFDR value as 5
      gsea_res_mat[gsea_res_mat == "Inf"] <- 5
    }else{
      gsea_res_mat[gsea_res_mat == "Inf"] <- round(max(gsea_res_mat[gsea_res_mat != "Inf"]))
    }
    gsea_res_list[[i]] <- gsea_res_mat
  }
  return(gsea_res_list)
}

###function of generating complexheatmap
PlotGseaHeatmap <- function(mat, direction, cluster_cell, title, ysize = 7.3, sfc = sfc){
  ###top anntation for cell grouping in heatmap body
  # add cell level2 label
  cell_level2 <- as.character(cluster_cell[gsub("(.*)_(.*)","\\2",colnames(mat)),"cell_level2"])
  names(cell_level2) <- colnames(mat)
  cell_level2 <- sort(cell_level2)
  cell_level2_col <- structure(names = unique(cell_level2), DefaulfColorPalette[1:length(unique(cell_level2))])
  ha.col <- columnAnnotation(
    Celltype_major_lineage = cell_level2,
    col = list(Celltype_major_lineage = cell_level2_col),
    annotation_name_side = "left",
    annotation_legend_param = list(
      Celltype_major_lineage = list(title = "Celltype (major-lineage)")
    )
  )
  
  ###left annotation for pathway category
  path_cl <- as.character(path_cat[rownames(mat),1])
  names(path_cl) <- rownames(mat)
  path_cl <- sort(path_cl)
  path_col <- structure(names = sort(as.character(unique(path_cat[,1]))), 
                        CatPlatte[1:length(unique(path_cat[,1]))])
  ha.row <- rowAnnotation(
    Pathway = path_cl,
    col = list(Pathway = path_col)
  )
  
  ###set main heatmap body color
  if(direction == "UP"){
    col_fun <- colorRamp2(c(0,max(mat)/2,max(mat)), c("#F2F2F2", "#FDBF6F", "#E31A1C"))
  }else{
    col_fun <- colorRamp2(c(0,max(mat)/2,max(mat)), c("#F2F2F2", "#9ECAE1", "#2171B5" )) #"#08519C"
  }
  
  ### heatmap body
  if(nrow(mat) >1){
    mat.new <- mat[names(path_cl),names(cell_level2)]
  } else {
    mat.new <- as.matrix(t(mat[names(path_cl),names(cell_level2)]))
    rownames(mat.new) <- rownames(mat)
  }
  # colnames(mat.new) <- paste(cluster_cell[colnames(mat.new),"cell_level2"], "_C",gsub("cluster_","",colnames(mat)), sep = "")
  ht_list = Heatmap(mat.new, name = "-log10FDR", # expression(-log[10]("FDR"))
                    col = col_fun,
                    cluster_rows = FALSE,
                    cluster_columns = FALSE,
                    show_column_dend = FALSE,
                    show_row_dend = FALSE,# rect_gp = gpar(col= "white"), 
                    show_column_names = TRUE,#row_split = g.group,
                    row_names_side = "left", 
                    row_names_gp = gpar(fontsize = ysize),
                    column_names_gp = gpar(fontsize = 10),
                    row_names_max_width = unit(7, "cm"),
                    top_annotation = ha.col,
                    left_annotation = ha.row,
                    column_title = title,
                    # column_title_gp = gpar(fontsize = tsize),
                    width = unit(ncol(mat.new), "cm"),
                    height = unit(nrow(mat.new)*sfc, "cm"),
                    # heatmap_width = unit(ncol(mat.new)+8, "cm"),
                    # heatmap_height = unit(nrow(mat.new)*0.7+5, "cm"),
                    use_raster = TRUE, raster_device = "png"
  )
  ###draw together(main heatmap, label bars)
  
  draw(ht_list, padding = unit(c(20, 2, 2, 2), "mm"), 
       merge_legends = TRUE, heatmap_legend_side = "right", 
       annotation_legend_side = "right") 
  ###add line for separating level3 cells
  if(length(table(cell_level2)) > 1){
    ini <- 0
    for(cc in table(cell_level2)[1:(length(table(cell_level2))-1)]){
      print (cc)
      ini <- ini + cc
      decorate_heatmap_body("-log10FDR", {
        i = ini
        x = i/ncol(mat)
        grid.lines(c(x, x), c(0, 1), gp = gpar(lwd = 2, lty = 2))
      })
    }
  }
}

### generating plots for each study with 4 figures (hallmark, kegg for up and down regulated)
PlotGSEA <- function(folder, type, outpath){
  ### read in cluster-cell annotation in the study folder
  cluster_cell <- read.table(dir(folder,pattern = "cluster_cell.txt",full.names = TRUE), sep = "\t", header = TRUE, row.names = 1)
  cc_rows <- paste("C", rownames(cluster_cell), sep = "") 
  cluster_cell <- cluster_cell %>% dplyr::mutate_all(as.character)
  rownames(cluster_cell) <- cc_rows
  
  ### get all gsea report files
  gsea_dir <- dir(paste(folder,type, sep = "/"), pattern = "gsea_report_for_na", full.names = TRUE)
  gsea_res_all <- merge_gsea_reports(gsea_dir= gsea_dir)
  split_gsea_list <- split_gsea_direction(gsea_res = gsea_res_all)
  
  ### generating two figures for up-regulated and down-regulated
  for (gsea_direction in c("UP","DOWN")){
    print(gsea_direction)
    if(gsea_direction == "UP"){
      gsea_mat <- as.matrix(split_gsea_list$pos)
    }else{
      gsea_mat <- as.matrix(split_gsea_list$neg)
    }
    title <- paste(gsea_direction, "-REGULATED ",toupper(type)," PATHWAYS", sep = "")
    ##complex heatmap
    hl <- 60*nrow(gsea_mat)+1200
    wl <- 110*ncol(gsea_mat)+2650
    tsize <- ifelse(nrow(gsea_mat)<=5, 8, 12)
    sfc <- ifelse(nrow(gsea_mat)<8, 0.8, 0.5)
    png(file = paste(outpath, folder,"_", type, "_",gsea_direction, "_heatmap.png",sep = ""), res = 300, height = hl, width = wl)
    p <- PlotGseaHeatmap(mat = gsea_mat, direction = gsea_direction, cluster_cell = cluster_cell, title = title, sfc = sfc)
    print(p)
    dev.off()
  }
}

