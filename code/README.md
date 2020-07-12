# Workflow to process tumor scRNA-seq data and prepare data for database

## 0. Download data
The analysis pipeline starts from count matrices and corresponding meta information (if available). 
The count matrices are usually downloaded from GEO. If there're only normalized count matrices like TPM or FPKM, they are also acceptable.
The meta information can be derived from supplementary file in GEO or original paper, Series Matrix file in GEO, and other sources.


## 1. Analyze data
### 1.1 Prepare data for MAESTRO pipeline
The analysis pipeline starts from a count matrix, which can be mtx, HDF5 or plain text formatted, and then performs QC, clustering and cell-type annotation.
The analysis pipeline will generate a R script which can be modified, clustering and annotated UMAP plots and a Seurat object which can be readable and writable.

The following commands can be used for format conversion.
```bash
MAESTRO mtx-to-h5           # Convert 10X mtx format matrix to HDF5 format.
MAESTRO mtx-to-count        # Convert 10X mtx format matrix to plain text count table.
MAESTRO count-to-h5         # Convert plain text count table to HDF5 format.
MAESTRO h5-to-count         # Convert HDF5 format to plain text count table.
MAESTRO merge-h5            # Merge 10X HDF5 files.
```

Meta data is optional, not required. If meta data is provided, it should be a table with cells as rows and meta information as columns. 
The first line of the meta data file should contain the names of the variables.

**Note:** If there're multiple samples (count matrices) in one dataset, usually we convert the count matrices to HDF5 format firstly. 
Then we merge these h5 matrices to a big h5 matrix and take it as the input of the analysis pipeline.
If meta table is provided, users should make sure the barcodes in the meta data are consistent with those in the count matrix.
Because in the big merged matix, the cell barcodes may have prefix (added through the parameter `--cellprefix` in `MAESTRO merge-h5`).

### 1.2 Run MAESTRO analysis pipeline
Here are some examples to run analysis pipeline.

**For mtx format data**
```
MAESTRO scrna-analysis --format mtx --matrix Data/GSE140228_UMI_counts_Droplet.mtx \
--feature Data/GSE140228_UMI_counts_Droplet_genes_noheader.tsv --gene-column 2 --barcode Data/GSE140228_UMI_counts_Droplet_barcodes.tsv \
--meta-file Data/GSE140228_Droplet_cellinfo.tsv --meta-sep tab --meta-cell 1 \
--count-cutoff 1000 --gene-cutoff 500 --assembly GRCh38 \
--directory . --outprefix LIHC_GSE140228_10X
```

**For h5 format data**
```
MAESTRO scrna-analysis --format h5 --matrix Data/GSE140228_Smartseq2_counts.h5 \
--meta-file Data/GSE140228_Smartseq2_cellinfo.tsv --meta-sep tab --meta-cell 1 \
--count-cutoff 1000 --gene-cutoff 500 --assembly GRCh38 \
--directory . --outprefix LIHC_GSE140228_Smartseq2
```

**For plain-text file**
```
MAESTRO scrna-analysis --format plain --matrix Data/GSE108989_CRC.TCell.S11138.count_nogeneid.txt --separator tab \
--count-cutoff 1000 --gene-cutoff 500 --assembly GRCh37 \
--directory . --outprefix COAD_GSE108989
```

### 1.3 Check and remove batch effect
After the analysis pipeline, the batch effect should be checked for each dataset. The batch effect usually comes from source, sample, patient, or cohort.
If batch effect exists, we should correct batch effect through `CCA`, which has been integrated to `RNABatchCorrect` function in MAESTRO.
```R
library(MAESTRO)
RNA.res <- RNABatchCorrect(RNA.res$RNA, RNA.res$RNA@meta.data$patient, 
                           nfeatures = 3000, dims.use = 1:30, cluster.res = 1, only.pos = TRUE, 
                           runpca.agrs = list(npcs = 50))
```

After batch effect removal, automatic cell-type annotation by MAESTRO shoule be re-done.
```R
RNA.res$RNA = RNAAnnotateCelltype(RNA = RNA.res$RNA, 
                                  genes = RNA.res$genes,
                                  signatures = "human.immune.CIBERSORT",
                                  min.score = 0.6)
saveRDS(RNA.res, "UCEC_GSE139555_CCA_res.rds")
```

### 1.4 Classify malignant cells and normal cells
For the unsorted data, we should distinguish normal cells from malignant cells. We can directly obtain the cell-type annotation from the original publication. 
If it's not availble, inferCNV can be used to identify malignant cells.
```R
library(inferCNV)
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
```

### 1.5 Correct cell-type annotation manually
After automatic cell-type annotation by MAESTRO, we should make some manual corrections to some tissue-specific cell types 
combining with original annotation and malignant cell identification in the previous step. 
For those rare cell types like pDC and mast cells, manual correction should be done based on expression of markers.
`VisualizeUmap` function in MAESTRO can be used to visualize the gene expression.
```R
VisualizeUmap(SeuratObj = RNA.res$RNA, type = "RNA", genes = c("HAVCR2", "LAG3", "PDCD1"), ncol = 3,
              width = 15, height = 4, name = paste0(RNA.res$RNA@project.name, "_CD8Tex"))
```

### 1.6 Level-1/level-3 annotation
All the cells are classified into three types, malignant cells, immune cells and stromal cells based on the major-lineage level annotation. 
To gain more detailed insights into immune cells, we need to generate the minor-lineage subtype annotation differentiating from major-lineage cell-types.
The scripts for level-1 and level-3 annotation can be found in `2_Annotation`.



