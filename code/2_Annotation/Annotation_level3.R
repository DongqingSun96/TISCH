library(MAESTRO)
library(Seurat)
library(ggplot2)
file_path="/mnt/Storage2/home/wangjin/scTumor_Data/"
file_names=list.files(file_path,recursive=T)
Seurat_file=Seurat_file[grep("_res.rds",Seurat_file)]
Seurat_file=paste0(file_path,Seurat_file)

result = sapply(Seurat_file, Level3_RNAAnnotateCelltype)

Level3_Tcell_RNAAnnotateCelltype <- function(subset_Tcell){
  signatures = read.table("Signature/Tcell_subset_signature.txt",header = F,sep="\t")
  
  celltypes <- as.character(unique(signatures[,1]))
  signature_list <- sapply(1:length(celltypes),function(x){
    return(toupper(as.character(signatures[which(signatures[,1]==celltypes[x]),2])))
  })
  names(signature_list) <- celltypes
  
  cluster_celltypes = sapply(as.numeric(as.vector(unlist(subset_Tcell$cluster_id))), function(x){
    if(subset_Tcell[match(x,as.numeric(as.vector(unlist(subset_Tcell$cluster_id)))),2] %in% c("CD4Tconv")){
      temp_signature_list=signature_list[c(2,5,7,10:12)]
    }else{
      temp_signature_list=signature_list[c(1,3,4,6,8)]
    }
    
    idx = genes$cluster==x
    avglogFC = genes$avg_logFC[idx]
    names(avglogFC) = toupper(genes$gene[idx])
    score_cluster = sapply(temp_signature_list, function(y){
      score = sum(avglogFC[y], na.rm = TRUE) / log2(length(y))
      return(score)
    })
    
    if(max(score_cluster, na.rm = TRUE)>0){
      cluster_celltypes = names(score_cluster)[which.max(score_cluster)]
    }else{
      index=which(seurat_object$RNA@meta.data$seurat_clusters == x)[1]
      cluster_celltypes = seurat_object$RNA@meta.data$assign.curated[index]}
  })
  
  return(cbind(as.numeric(as.vector(unlist(subset_Tcell$cluster_id))),cluster_celltypes))
}


Level3_DC_RNAAnnotateCelltype <- function(subset_DC){
  signatures = read.table("Signature/DC_subset_signature.txt",header = F,sep="\t")
  
  celltypes <- as.character(unique(signatures[,1]))
  signature_list <- sapply(1:length(celltypes),function(x){
    return(toupper(as.character(signatures[which(signatures[,1]==celltypes[x]),2])))
  })
  names(signature_list) <- celltypes
  signature_list=signature_list[1:5]#exclude pDC 
  cluster_celltypes = sapply(as.integer(unique(subset_DC$seurat_clusters))-1, function(x){
    idx = genes$cluster==x
    avglogFC = genes$avg_logFC[idx]
    names(avglogFC) = toupper(genes$gene[idx])
    score_cluster = sapply(signature_list, function(y){
      score = sum(avglogFC[y], na.rm = TRUE) / log2(length(y))
      return(score)
    })
    if(max(score_cluster, na.rm = TRUE)>0){
      cluster_celltypes = names(score_cluster)[which.max(score_cluster)]
    }else{
      index=which(seurat_object$RNA@meta.data$seurat_clusters == x)[1]
      cluster_celltypes = seurat_object$RNA@meta.data$assign.curated[index]}
  })
  
  return(cbind(as.integer(unique(subset_DC$seurat_clusters))-1,cluster_celltypes))
}


Level3_RNAAnnotateCelltype<-function(file_name){
  seurat_object<-readRDS(file_name)
  genes<-seurat_object$genes
  dir_name=dirname(file_name)
  setwd(dir_name)

  if(length(seurat_object$RNA@meta.data$assign.curated) > 0){
    cluster_id=as.integer(unique(seurat_object$RNA@meta.data$seurat_clusters))-1
    level3_annotation=data.frame(cbind(cluster_id,seurat_object$RNA@meta.data$assign.curated[match(cluster_id,seurat_object$RNA@meta.data$seurat_clusters)]))
    names(level3_annotation)=c("cluster_id","level2_anno")
    
    subset_Tcell=subset(level3_annotation,level2_anno %in% c("CD8T","CD4Tconv"))
    Tcell_annotation=Level3_Tcell_RNAAnnotateCelltype(subset_Tcell)

    subset_DC=subset(seurat_object$RNA@meta.data,assign.curated %in% c("Mono/Macro","DC"))
    DC_Mo_annotation=Level3_DC_RNAAnnotateCelltype(subset_DC)

    level3_anno=rbind(Tcell_annotation,DC_Mo_annotation)
    level3_annotation=as.matrix(level3_annotation)
    if(dim(level3_anno)[1] > 1){
      level3_anno=matrix(unlist(level3_anno),byrow=F,ncol=2)
      level3_annotation[match(level3_anno[,1],level3_annotation[,1]),2]=level3_anno[,2]
    }else{
      level3_annotation[match(unlist(level3_anno[1]),level3_annotation[,1]),2]=unlist(level3_anno[2])
    }
    
    current.cluster.ids = level3_annotation[,1]
    new.cluster.ids = level3_annotation[,2]
    seurat_object$RNA@meta.data$assign.level3_anno = Idents(seurat_object$RNA)[rownames(seurat_object$RNA@meta.data)]
    seurat_object$RNA@meta.data$assign.level3_anno = plyr::mapvalues(x = seurat_object$RNA@meta.data$assign.level3_anno,
                                                                     from = current.cluster.ids, to = new.cluster.ids)
    
    p = DimPlot(object = seurat_object$RNA, group = "assign.level3_anno", label = TRUE, pt.size = 0.1)
    ggsave(file.path(paste0(seurat_object$RNA@project.name, "_", "annotated_level3", ".png")), p,  width=6.5, height=5)
    saveRDS(seurat_object, paste0(seurat_object$RNA@project.name,"_res.rds"))
  }
}