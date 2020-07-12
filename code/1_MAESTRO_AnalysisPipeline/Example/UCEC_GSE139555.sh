# @Author: Dongqing Sun
# @Date:   2020-04-25 04:55:38
# @Last Modified by:   Dongqing Sun
# @Last Modified time: 2020-07-12 19:35:04


# Sample type: LECR(Lung, Endometrial, Colon, Renal)
# Genome build: hg38
# Celltype: CD45+ (select from all, CD45+, CD3+)
# Meta data: yes

# pre-process meta data
awk 'BEGIN{FS="\t"; OFS="\t"} {print $1,$5,$6,$7}' Data/LECR_GSE139555_metadata.txt | sed 's/_/@/g' > Data/LECR_GSE139555_meta.txt

# run analysis pipeline
MAESTRO scrna-analysis --format h5 --matrix Data/LECR_GSE139555_UCEC_gene_count.h5 \
--meta-file Data/LECR_GSE139555_meta.txt --meta-sep tab --meta-cell 1 \
--count-cutoff 1000 --gene-cutoff 500 --assembly GRCh38 \
--directory . --outprefix UCEC_GSE139555
