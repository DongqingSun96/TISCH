library(MAESTRO)
library(Seurat)
library(ggplot2)
file_path="/mnt/Storage2/home/wangjin/scTumor_Data/"
file_names=list.files(file_path,recursive=T)
Seurat_file=Seurat_file[grep("_res.rds",Seurat_file)]
Seurat_file=paste0(file_path,Seurat_file)
result = sapply(Seurat_file, Level1_RNAAnnotateCelltype)

Level1_RNAAnnotateCelltype<-function(file_name, min.score = 0){
  seurat_object <- readRDS(file_name)
  dir_name=dirname(file_name)
  setwd(dir_name)
  
  if("assign.curated" %in% colnames(seurat_object$RNA@meta.data)){
    cluster_id=as.integer(unique(seurat_object$RNA@meta.data$seurat_clusters))-1
    level1_annotation=data.frame(cbind(cluster_id,seurat_object$RNA@meta.data$assign.curated[match(cluster_id,seurat_object$RNA@meta.data$seurat_clusters)]))
    names(level1_annotation)=c("cluster_id","level2_anno")
    
    level2_immu=c("B","CD4Tconv","CD8T","CD8Tex","DC","Mast","Mono/Macro","TMKI67","Neutrophils","NK","Plasma","Treg","pDC","EryPro","GMP","Progenitor","Promonocyte","HSC","ILC","hematopoietic stem/progenitor cell")
    malignant_cell=c("Malignant","OPC-like Malignant","AC-like Malignant","OC-like Malignant","NB-like Malignant","Pvalb-like Maligant","Vip-like Malignant","Astro-like Malignant","Endo-like Malignant")
    others_cell=c("Oligodendrocyte","Oligodendrocytes","Neuron","OPC","Alveolar", "Endocrine","Others","Stellate","Astocyte","Acinar","Ductal","Astrocytes","Acinar cells","Microglia","Oligo Opalin")
    
    level1_annotation=as.matrix(level1_annotation)
    level1_annotation[which(!(level1_annotation[,2] %in% c(level2_immu,malignant_cell,others_cell))),2]="Stromal cells"
    level1_annotation[which(level1_annotation[,2] %in% level2_immu),2]="Immune cells"
    level1_annotation[which(level1_annotation[,2] %in% malignant_cell ),2]="Malignant cells"
    level1_annotation[which(level1_annotation[,2] %in% others_cell),2]="Others"
    level2_ann=seurat_object$RNA@meta.data$assign.curated[match(cluster_id,seurat_object$RNA@meta.data$seurat_clusters)]
    print(cbind(level1_annotation,level2_ann))
    
    current.cluster.ids = level1_annotation[,1]
    new.cluster.ids = level1_annotation[,2]
    seurat_object$RNA@meta.data$assign.level1_anno = Idents(seurat_object$RNA)[rownames(seurat_object$RNA@meta.data)]
    seurat_object$RNA@meta.data$assign.level1_anno = plyr::mapvalues(x = seurat_object$RNA@meta.data$assign.level1_anno,
                                                                     from = current.cluster.ids, to = new.cluster.ids)
    
    p = DimPlot(object = seurat_object$RNA, group = "assign.level1_anno", label = TRUE, pt.size = 0.1)
    ggsave(file.path(paste0(seurat_object$RNA@project.name, "_", "annotated_level1", ".png")), p,  width=7, height=5)
    saveRDS(seurat_object, paste0(seurat_object$RNA@project.name,"_res.rds"))
  }
}