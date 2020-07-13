-- MySQL dump 10.13  Distrib 8.0.20, for Linux (x86_64)
--
-- Host: localhost    Database: tisch_beta
-- ------------------------------------------------------
-- Server version	8.0.20

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `LinkData_datacollect`
--

DROP TABLE IF EXISTS `LinkData_datacollect`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LinkData_datacollect` (
  `Dataset Name` varchar(100) NOT NULL,
  `Cancer Type` varchar(50) NOT NULL,
  `Platform` varchar(50) NOT NULL,
  `Patient Number` int DEFAULT NULL,
  `Cell Number` int NOT NULL,
  `Publication` varchar(100) NOT NULL,
  `PMID` varchar(20) NOT NULL,
  `Dataset ID` varchar(50) NOT NULL,
  `Dataset Type` varchar(20) NOT NULL,
  `Species` varchar(20) NOT NULL,
  `Cell Type` varchar(1000) NOT NULL,
  `Primary` varchar(50) NOT NULL,
  `Treatment` varchar(50) NOT NULL,
  `Detailed Treatment` varchar(50) NOT NULL,
  PRIMARY KEY (`Dataset Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LinkData_datacollect`
--

LOCK TABLES `LinkData_datacollect` WRITE;
/*!40000 ALTER TABLE `LinkData_datacollect` DISABLE KEYS */;
INSERT INTO `LinkData_datacollect` VALUES ('AEL_GSE142213','AEL','10x Genomics',2,3994,'Di Genua C, et al. Cancer Cell 2020','32330454','GSE142213','TME','Human','Malignant, Mono/Macro, NK, Plasma','Primary','None','None\r'),('AEL_GSE142213_mouse','AEL','10x Genomics',2,9595,'Di Genua C, et al. Cancer Cell 2020','32330454','GSE142213','TME','Mouse','Malignant, Mono/Macro, Neutrophils, NK','Primary','None','None\r'),('ALL_GSE132509','ALL','10x Genomics',11,37936,'Caron M, et al. Sci Rep 2020','32415257','GSE132509','TME','Human','B, CD4Tconv, CD8T, Erythrocytes, Malignant, Mono/Macro, TMKI67','Primary','None','None\r'),('AML_GSE116256','AML','Smart-seq2',21,38348,'De Bie J, et al. Leukemia 2018','29740158','GSE116256','TME','Human','B, CD4Tconv, CD8T, EryPro, GMP, HSC, Malignant, Mono/Macro, NK, Plasma, Progenitor, Promonocyte, TMKI67','Primary','None','None\r'),('AML_GSE147989','AML','10x Genomics',2,7389,'NA','NA','GSE147989','TME','Human','HSC','Primary','Targeted therapy','Targeted therapy (Cusatuzumab)\r'),('BCC_GSE123813_aPD1','BCC','10x Genomics',11,52884,'Yost KE, et al. Nat Med 2019','31359002','GSE123813','ICB','Human','B, CD4Tconv, CD8T, CD8Tex, DC, Endothelial, Fibroblasts, Malignant, Mast, Melanocytes, Mono/Macro, Myofibroblasts, NK, Plasma, TMKI67, Treg, pDC','Metastatic','Immunotherapy','aPD1\r'),('BLCA_GSE130001','BLCA','10x Genomics',2,4129,'Wang L, et al. Genome Med 2020','32111252','GSE130001','TME','Human','Endothelial, Epithelial, Fibroblasts, Myofibroblasts','Primary','None','None\r'),('BLCA_GSE145281_aPD1','BLCA','10x Genomics',10,14462,'Yuen KC, et al. Nat Medicine 2020','32405063','GSE145281','ICB','Human','B, CD4Tconv, CD8T, DC, Mono/Macro, NK','Metastatic','Immunotherapy','aPD1\r'),('BRCA_Alex','BRCA','10x Genomics',26,89471,'NA','NA','NA','TME','Human','B, CD4Tconv, CD8Tex, Endothelial, Fibroblasts, Malignant, Mono/Macro, Plasma, SMC, TMKI67, pDC','Primary','None','None\r'),('BRCA_GSE110686','BRCA (TNBC)','10x Genomics',2,6035,'Savas P, et al. Nat Med 2018','29942092','GSE110686','TME','Human','CD4Tconv, CD8T, CD8Tex, Mono/Macro, TMKI67, Treg','Primary, Metastatic','None','None\r'),('BRCA_GSE114727_10X','BRCA','10x Genomics',3,28678,'Azizi E, et al. Cell 2018','29961579','GSE114727','TME','Human','CD4Tconv, CD8T, CD8Tex, TMKI67, Treg','Primary','None','None\r'),('BRCA_GSE114727_inDrop','BRCA','inDrop',8,19676,'Azizi E, et al. Cell 2018','29961579','GSE114727','TME','Human','B, CD4Tconv, CD8T, CD8Tex, DC, Endothelial, Fibroblasts, Mast, Mono/Macro, Myofibroblasts, NK, TMKI67, Treg, pDC','Primary','None','None\r'),('BRCA_GSE136206_mouse_aPD1aCTLA4','BRCA','10x Genomics',0,27532,'Hollern DP, et al. Cell 2019','31730857','GSE136206','ICB','Mouse','B, CD4Tconv, CD8T, CD8Tex, DC, Endothelial, Malignant, Mono/Macro, NK, Neutrophils, Plasma, TMKI67','Primary','Immunotherapy','aPD1 + aCTLA4\r'),('BRCA_GSE138536','BRCA','Smart-seq2',8,1902,'Gulati GS, et al. Science 2020','31974247','GSE138536','TME','Human','Epithelial, Fibroblasts, Mono/Macro, Myofibroblasts','Primary','None','None\r'),('BRCA_GSE143423','BRCA','10x Genomics',2,4375,'Weilin Jin, et al.','Preprint','GSE143423','TME','Human','Malignant, Mono/Macro, Oligodendrocyte','Metastatic','None','None\r'),('BRCA_SRP114962','BRCA','SNRS',8,2472,'Kim C, et al. Cell 2018','29681456','SRP114962','TME','Human','CD8Tex, Malignant','Primary','Chemotherapy','Chemotherapy\r'),('CHOL_GSE125449_aPD1aPDL1aCTLA4','CHOL','10x Genomics',10,5761,'Lichun Ma, et al. Cancer Cell 2019','31588021','GSE125449','ICB','Human','B, CD4Tconv, CD8T, CD8Tex, Endothelial, Fibroblasts, Hepatic progenitor, Malignant, Mono/Macro, Plasma, TMKI67','Primary','Immunotherapy','aPD1 + aPDL1 + aCTLA4\r'),('CLL_GSE111014','CLL','10x Genomics',4,30106,'Rendeiro AF, et al. Nat Commun 2020','31996669','GSE111014','TME','Human','B, CD4Tconv, CD8T, Mono/Macro, pDC, TMKI67','Primary','Targeted therapy','Targeted therapy (Ibrutinib)\r'),('CLL_GSE125881','CLL, NHL','10x Genomics',4,60528,'Sheih A, et al. Nat Commun 2020','31924795','GSE125881','TME','Human','CD8T, CD8Tex, TMKI67','Primary','Immunotherapy','Adoptive cell therapy (CAR-T)\r'),('COAD_GSE108989','COAD','Smart-seq2',12,11125,'Zhang L, et al. Nature 2018','30479382','GSE108989','TME','Human','CD4Tconv, CD8T, CD8Tex, TMKI67, Treg','Primary','None','None\r'),('COAD_GSE112865_mouse_aPD1','COAD','10x Genomics',0,4454,'Arlauckas SP, et al. Theranostics 2018','30613266','GSE112865','ICB','Mouse','CD4Tconv, CD8T, CD8Tex, DC, Mono/Macro, NK, Neutrophils, TMKI67, pDC','Primary','Immunotherapy','aPD1\r'),('COAD_GSE120909_mouse_aPD1','COAD','Smart-seq',0,1881,'Wang B, et al. Sci Immunol 2018','30389797','GSE120909','ICB','Mouse','CD8T, CD8Tex, DC, Mono/Macro, Neutrophils, pDC','Primary','Immunotherapy','aPD1\r'),('COAD_GSE122969_mouse_aPD1aTIM3','COAD','10x Genomics',0,5457,'Kurtulus S, et al. Immunity 2019','30635236','GSE122969','ICB','Mouse','CD8T, CD8Tex, Fibroblasts, Mono/Macro, TMKI67, pDC','Primary','Immunotherapy','aPD1 + aTIM3\r'),('COAD_GSE136394','COAD, READ','10x Genomics',5,67171,'Lu YC, et al.Cancer Immunol Res 2019','31484655','GSE136394','TME','Human','CD4Tconv, CD8T, Mono/Macro, TMKI67','Primary, Metastatic','Immunotherapy','Adoptive cell therapy (TIL)\r'),('COAD_GSE139555','COAD','10x Genomics',2,10112,'Wu TD, et al. Nature 2020','32103181','GSE139555','TME','Human','B, CD4Tconv, CD8T, CD8Tex, Mast, Mono/Macro, Myofibroblasts, NK, Plasma, TMKI67, Treg','Primary','None','None\r'),('COAD_GSE146771_10X','COAD','10x Genomics',10,43817,'Zhang L, et al. Cell 2020','32302573','GSE146771','TME','Human','B, CD4Tconv, CD8T, CD8Tex, Mast, Mono/Macro, TMKI67','Primary','None','None\r'),('COAD_GSE146771_Smartseq2','COAD','Smart-seq2',10,10468,'Zhang L, et al. Cell 2020','32302573','GSE146771','TME','Human','B, CD4Tconv, CD8T, CD8Tex, Fibroblasts, Malignant, Mast, Mono/Macro, NK, TMKI67, Treg','Primary','None','None\r'),('GBM_GSE102130','GBM','Smart-seq2',6,3321,'Filbin MG, et al. Science 2018','29674595','GSE102130','TME','Human','AC-like Malignant, Mono/Macro, OC-like Malignant, OPC-like Malignant, Oligodendrocyte','Primary','None','None\r'),('GBM_GSE103224','GBM','Microwell',8,17185,'Yuan J, et al. Genome Med 2018','30041684','GSE103224','TME','Human','AC-like Malignant, Endothelial, Mono/Macro, NB-like Malignant, Neuron, OC-like Malignant, OPC-like Malignant','Primary','None','None\r'),('GBM_GSE131928_10X','GBM','10x Genomics',9,13553,'Neftel C, et al. Cell 2019','31327527','GSE131928','TME','Human','AC-like Malignant, CD8Tex, Malignant, Mono/Macro, Oligodendrocyte, OPC-like Malignant','Primary','None','None\r'),('GBM_GSE131928_Smartseq2','GBM','Smart-seq2',28,7930,'Neftel C, et al. Cell 2019','31327527','GSE131928','TME','Human','AC-like Malignant, CD8T, CD8Tex, Malignant, Oligodendrocyte, OPC-like Malignant','Primary','None','None\r'),('GBM_GSE135437','GBM','mCEL-Seq2',19,12559,'Sankowski R, et al. Nat Neurosci 2019','31740814','GSE135437','TME','Human','CD8T, Microglia, Mono/Macro, Oligodendrocyte','Primary, Metastatic','None','None\r'),('GBM_GSE138794','GBM','10x Genomics',9,18458,'Wang L, et al. Cancer Discov 2019','31554641','GSE138794','TME','Human','Astrocyte, Endothelial, Malignant, Mono/Macro, Oligodendrocyte','Primary','None','None\r'),('GBM_GSE139448','GBM','10x Genomics',3,12152,'Wang R, et al. Stem Cell Reports 2020','32004492','GSE139448','TME','Human','Endothelial, Malignant, Mast, Mono/Macro','Primary','None','None\r'),('GBM_GSE141982','GBM','10x Genomics',2,5263,'Wang L, et al. Bioinformatics 2020','32105316','GSE141982','TME','Human','CD8T, Endothelial, Malignant, Mono/Macro','Primary','None','None\r'),('GBM_GSE148842','GBM','Microwell',7,111397,'NA','Preprint','GSE148842','TME','Human','AC-like Malignant, CD8Tex, Malignant, Mono/Macro, Oligodendrocyte, Others','Primary','None','None\r'),('GBM_GSE70630','GBM','Smart-seq2',6,4347,'Tirosh I, et al. Nature 2016','27806376','GSE70630','TME','Human','AC-like Malignant, Mono/Macro, OC-like Malignant, Oligodendrocyte','Primary','None','None\r'),('GBM_GSE84465','GBM','Smart-seq2',4,3533,'Darmanis S, et al. Cell Rep 2017','29091775','GSE84465','TME','Human','AC-like Malignant, Astrocyte, Malignant, Mono/Macro, Neuron, OPC, Oligodendrocyte, Vascular','Primary','None','None\r'),('GBM_GSE89567','GBM','Smart-seq2',10,6341,'Venteicher AS, et al. Science 2017','28360267','GSE89567','TME','Human','AC-like Malignant, Mono/Macro, OC-like Malignant, Oligodendrocyte','Primary','None','None\r'),('HNSC_GSE103322','HNSC','Smart-seq2',18,5902,'Puram SV, et al. Cell 2018','29198524','GSE103322','TME','Human','CD4Tconv, CD8T, CD8Tex, Endothelial, Fibroblasts, Malignant, Mast, Mono/Macro, Myfibroblasts, Myocyte, Plasma','Primary','None','None\r'),('HNSC_GSE139324','HNSC','10x Genomics',26,130721,'Cillo AR, et al. Immunity 2020','31924475','GSE139324','TME','Human','B, CD4Tconv, CD8T, CD8Tex, Mast, Mono/Macro, NK, Plasma, TMKI67, Treg, pDC','Primary','None','None\r'),('KIRC_GSE111360','KIRC','10x Genomics',2,23130,'Neal JT, et al. Cell 2018','30550791','GSE111360','TME','Human','B, CD4Tconv, CD8T, CD8Tex, DC, Fibroblasts, Mast, Mono/Macro, NK, Plasma, TMKI67, Treg','Primary','None','None\r'),('KIRC_GSE139555','KIRC','10x Genomics',3,49907,'Wu TD, et al. Nature 2020','32103181','GSE139556','TME','Human','B, CD4Tconv, CD8T, CD8Tex, DC, Endothelial, Mast, Mono/Macro, NK, Plasma, TMKI67, pDC','Primary','None','None\r'),('KIRC_GSE145281_aPD1','KIRC','10x Genomics',4,44220,'Yuen KC, et al. Nat Medicine 2020','32405063','GSE145281','ICB','Human','B, CD4Tconv, CD8T, DC, Mono/Macro, Myofibroblasts, NK, Plasma','Metastatic','Immunotherapy','aPD1\r'),('LIHC_GSE125449_aPDL1aCTLA4','LIHC','10x Genomics',9,3834,'Ma L, et al.Cancer Cell 2019','31588021','GSE125449','ICB','Human','B, CD8Tex, Endothelial, Fibroblasts, Hepatic progenitor, Malignant, Mono/Macro, Plasma','Primary','Immunotherapy','aPDL1 + aCTLA4\r'),('LIHC_GSE140228_10X','LIHC','10x Genomics',5,62530,'Zhang Q, et al. Cell 2019','31675496','GSE140228','TME','Human','B, CD4Tconv, CD8T, CD8Tex, DC, ILC, Mast, Mono/Macro, NK, Plasma, TMKI67, Treg','Primary','None','None\r'),('LIHC_GSE140228_Smartseq2','LIHC','Smart-seq2',6,7074,'Zhang Q, et al. Cell 2019','31675496','GSE140228','TME','Human','B, CD4Tconv, CD8Tex, DC, ILC, Mast, Mono/Macro, NK, Plasma, TMKI67','Primary','None','None\r'),('LIHC_GSE98638','LIHC','Smart-seq2',6,5059,'Zheng C, et al. Cell 2017','28622514','GSE98638','TME','Human','CD4Tconv, CD8T, CD8Tex, Others, TMKI67, Treg','Primary','None','None\r'),('MB_GSE119926','MB','Smart-seq2',25,7745,'Hovestadt V, et al. Nature 2019','31341285','GSE119926','TME','Human','Fibroblasts, Malignant, TMKI67','Primary, Metastatic','None','None\r'),('MCC_GSE117988_aPD1aCTLA4','MCC','10x Genomics',1,10134,'Paulson KG et al. Nat Commun 2018','30250229','GSE117988','ICB','Human','B, CD4Tconv, CD8T, CD8Tex, Fibroblasts, Malignant, Mono/Macro, Others','Metastatic','Immunotherapy','T cell therapy, aPD1 + aCTLA4\r'),('MCC_GSE118056_aPDL1','MCC','10x Genomics',1,11024,'Paulson KG, et al. Nat Commun 2018','30250229','GSE118056','ICB','Human','B, CD4Tconv, CD8T, Malignant, Mono/Macro, Myofibroblasts, NK, Others, pDC, TMKI67, Treg','Primary','Immunotherapy','T cell therapy, aPDL1\r'),('MM_GSE117156','MM','MARS-seq',14,24918,'Ledergor G, et al. Nat Med 2018','30523328','GSE117156','TME','Human','CD8T, Malignant, Mono/Macro, Plasma','Primary','Targeted therapy','Targeted therapy (Bortezomib)\r'),('MM_GSE141299','MM','10x Genomics',7,16840,'NA','NA','GSE141299','TME','Human','Malignant','Primary','None','None\r'),('NET_GSE140312','NET','10x Genomics',1,3158,'Rao M, et al. Cold Spring Harb Mol Case Stud 2020','32054662','GSE140312','TME','Human','Endothelial, Fibroblasts, Mono/Macro, Myofibroblasts, Others','Primary, Metastatic','None','None\r'),('NHL_GSE128531','NHL','10x Genomics',9,30497,'Gaydosik AM, et al. Clin Cancer Res 2019','31010835','GSE128531','TME','Human','B, CD4Tconv, CD8Tex, Endothelial, Fibroblasts, Keratinocytes, Melanocytes, Mono/Macro, NK, Others, Pericytes, Secretory glandular, SMC, TMKI67','Primary','None','None\r'),('NSCLC_EMTAB6149','NSCLC','10x Genomics',5,40218,'Lambrechts D, et al. Nat Med 2018','29988129','EMTAB6149','TME','Human','Alveolar, B, CD4Tconv, CD8T, CD8Tex, Endothelial, Fibroblasts, Malignant, Mast, Mono/Macro, Plasma, Treg','Primary','None','None\r'),('NSCLC_GSE117570','NSCLC','10x Genomics',4,11453,'Song Q, et al. Cancer Med 2019','31033233','GSE117570','TME','Human','B, CD4Tconv, CD8T, DC, Endothelial, Malignant, Mast, Mono/Macro, Myofibroblasts, NK, Plasma','Primary','None','None\r'),('NSCLC_GSE127465','NSCLC','Smart-seq2',7,31179,'Zilionis R, et al. Immunity 2019','30979687','GSE127465','TME','Human','B, CD4Tconv, CD8Tex, DC, Endothelial, Fibroblasts, Malignant, Mast, Mono/Macro, NK, Neutrophils, Plasma','Primary','None','None\r'),('NSCLC_GSE127471','NSCLC','10x Genomics',1,1108,'Newman AM, et al. Nat Biotechnol 2019','31061481','GSE127471','TME','Human','B, CD4Tconv, CD8T, CD8Tex, Mono/Macro, NK, Others','Primary','None','None\r'),('NSCLC_GSE131907','NSCLC','10x Genomics',44,203298,'Kim N, et al. Nat Commun 2020','32385277','GSE131907','TME','Human','B, CD4Tconv, CD8T, CD8Tex, DC, Endothelial, Epithelial, Fibroblasts, Mast, Mono/Macro, Oligodendrocyte, pDC, Plasma','Primary, Metastatic','None','None\r'),('NSCLC_GSE139555','NSCLC','10x Genomics',6,78829,'Wu TD, et al. Nature 2020','32103181','GSE139557','TME','Human','B, CD4Tconv, CD8T, CD8Tex, DC, Mono/Macro, Myofibroblasts, Plasma, TMKI67, Treg, pDC','Primary','None','None\r'),('NSCLC_GSE143423','NSCLC','10x Genomics',3,12193,'Wang L, et al.','Preprint','GSE143423','TME','Human','CD8T, Endothelial, Malignant, Mono/Macro, Oligodendrocyte, Pericytes, Plasma','Metastatic','None','None\r'),('NSCLC_GSE99254','NSCLC','Smart-seq2',14,12346,'Guo X, et al. Nat Med 2018','29942094','GSE99254','TME','Human','CD4Tconv, CD8T, CD8Tex, Mono/Macro, TMKI67, Treg','Primary','None','None\r'),('OV_GSE115007','OV','10x Genomics',1,6000,'Tang-Huau TL, et al. Nat Commun 2018','29967419','GSE115007','TME','Human','DC, Mono/Macro, Plasma','Primary','None','None\r'),('OV_GSE118828','OV','Smart-seq2',9,1909,'Shih AJ, et al. PLoS One 2018','30383866','GSE118828','TME','Human','CD4Tconv, Endothelial, Fibroblasts, Malignant, Mono/Macro, Myofibroblasts','Primary, Metastatic','None','None\r'),('PAAD_CRA001160','PAAD (PDAC)','10x Genomics',35,57443,'Peng J, et al. Cell Res 2019','31273297','CRA001160','TME','Human','Acinar, B, CD8Tex, Ductal, Endocrine, Endothelial, Fibroblasts, Malignant, Mono/Macro, Plasma, Stellate, pDC','Primary','None','None\r'),('PAAD_GSE111672','PAAD','inDrop',3,6122,'Moncada R, et al. Nat Biotechnol 2020','31932730','GSE111672','TME','Human','Acinar, CD8T, Ductal, Endothelial, Fibroblasts, Malignant, Mast, Mono/Macro, Neutrophils, Others, TMKI67','Primary','None','None\r'),('PBMC_30K_10X','PBMC','10x Genomics',1,29079,'NA','NA','NA','Normal','Human','B, CD4Tconv, CD8T, DC, Mono/Macro, NK, pDC, Plasma, TMKI67','Normal','None','None\r'),('PBMC_60K_10X','PBMC','10x Genomics',1,63628,'NA','NA','NA','Normal','Human','B, CD4Tconv, CD8T, DC, Mono/Macro, NK, pDC','Normal','None','None\r'),('PBMC_8K_10X','PBMC','10x Genomics',1,8488,'NA','NA','NA','Normal','Human','B, CD4Tconv, CD8T, DC, Mono/Macro, NK, pDC','Normal','None','None\r'),('SARC_GSE119352_mouse_aPD1aCTLA4','SARC','10x Genomics',0,13789,'Gubin MM, et al. Cell 2018','30343900','GSE119352','ICB','Mouse','CD4Tconv, CD8T, DC, Fibroblasts, Mono/Macro, NK, TMKI67, pDC','Primary','Immunotherapy','aPD1 + aCTLA4\r'),('SCC_GSE123813_aPD1','SCC','10x Genomics',4,25891,'Yost KE, et al. Nat Med 2019','31359002','GSE123813','ICB','Human','CD4Tconv, CD8T, CD8Tex, TMKI67, Treg','Metastatic','Immunotherapy','aPD1\r'),('SKCM_GSE115978_aPD1','SKCM','Smart-seq2',31,7186,'Jerby-Arnon L, et al. Cell 2018','30388455','GSE115978','ICB','Human','B, CD4Tconv, CD8Tex, Endothelial, Fibroblasts, Malignant, Mono/Macro, NK, TMKI67','Primary, Metastatic','Immunotherapy','aPD1\r'),('SKCM_GSE120575_aPD1aCTLA4','SKCM','Smart-seq2',48,16291,'Sade-Feldman M, et al. Cell 2018','30388456','GSE120575','ICB','Human','B, CD4Tconv, CD8T, CD8Tex, Mono/Macro, NK, Plasma, TMKI67, Treg, pDC','Metastatic','Immunotherapy','aPD1 + aCTLA4\r'),('SKCM_GSE123139','SKCM','MARS-seq',25,35494,'Li H, et al. Cell 2019','30595452','GSE123139','TME','Human','B, CD4Tconv, CD8Tex, DC, Fibroblasts, Mono/Macro, Plasma, TMKI67, pDC','Primary, Metastatic','None','None\r'),('SKCM_GSE139249','SKCM','10x Genomics',4,39884,'de Andrade LF, et al. JCI Insight 2019','31801909','GSE139249','TME','Human','B, CD4Tconv, CD8Tex, Mono/Macro, Myofibroblasts, NK, Treg, pDC','Metastatic','None','None\r'),('SKCM_GSE148190','SKCM','10x Genomics',3,27834,'NA','NA','GSE148190','TME','Human','B, CD4Tconv, CD8T, CD8Tex, Mono/Macro, NK, Others, Treg','Metastatic','None','None\r'),('SKCM_GSE72056','SKCM','Smart-seq2',19,4645,'Tirosh I, et al. Science 2016','27124452','GSE72056','TME','Human','B, CD4Tconv, CD8Tex, Endothelial, Fibroblasts, Malignant, Mono/Macro, TMKI67','Metastatic','None','None\r'),('STAD_GSE134520','STAD','10x Genomics',13,41554,'Zhang P, et al. Cell 2019','31067475','GSE134520','TME','Human','CD8T, DC, Fibroblasts, Gland mucous, Malignant, Mast, Myofibroblasts, Pit mucous, Plasma','Primary','None','None\r'),('UCEC_GSE139555','UCEC','10x Genomics',3,12758,'Wu TD, et al. Nature 2020','32103181','GSE139558','TME','Human','CD4Tconv, CD8T, CD8Tex, Fibroblasts, TMKI67, Treg','Primary','None','None\r'),('UVM_GSE139829','UVM','10x Genomics',11,103703,'Durante MA, et al. Nat Commun 2020','31980621','GSE139829','TME','Human','B, CD4Tconv, CD8T, CD8Tex, Endothelial, Malignant, Mono/Macro, Plasma','Primary, Metastatic','None','None');
/*!40000 ALTER TABLE `LinkData_datacollect` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LinkData_uploadgenefile`
--

DROP TABLE IF EXISTS `LinkData_uploadgenefile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LinkData_uploadgenefile` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Gene File` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LinkData_uploadgenefile`
--

LOCK TABLES `LinkData_uploadgenefile` WRITE;
/*!40000 ALTER TABLE `LinkData_uploadgenefile` DISABLE KEYS */;
INSERT INTO `LinkData_uploadgenefile` VALUES (1,'upload/Exhaust_Dmg5yY1.txt'),(2,'upload/Exhaust_HrNXVZS.txt'),(3,'upload/6_XVoTZxy.txt'),(4,'upload/6_OGQKZgB.txt'),(5,'upload/6_9qTMrhh.txt'),(6,'upload/Exhaust_Mk4ObcG.txt'),(7,'upload/Exhaust_tkfuqNm.txt'),(8,'upload/Exhaust_3XASVxQ.txt'),(9,'upload/Exhaust_kGnX0rc.txt'),(10,'upload/Exhaust_ROjL291.txt'),(11,'upload/Exhaust_fIXgoKj.txt'),(12,'upload/Exhaust_NcjYVRY.txt'),(13,'upload/Exhaust_Bye0QuN.txt'),(14,'upload/Exhaust_U6yaGtp.txt'),(15,'upload/Exhaust_TVhOH35.txt'),(16,'upload/Exhaust_30GaZ6j.txt'),(17,'upload/Exhaust_R7PCdoE.txt'),(18,'upload/Exhaust_SP2gFuZ.txt'),(19,'upload/Exhaust_D45QX4o.txt'),(20,'upload/Exhaust_9Pjy5VF.txt'),(21,'upload/Exhaust_ObatR2J.txt'),(22,'upload/Exhaust_fdO9gT9.txt'),(23,'upload/Exhaust_BlySVUR.txt'),(24,'upload/Exhaust_qZfjMak.txt'),(25,'upload/Exhaust_fAzXyNa.txt'),(26,'upload/Exhaust_AAj2EUd.txt'),(27,'upload/6_WgwFytB.txt'),(28,'upload/6_R6n7pi5.txt'),(29,'upload/6_OX3awmN.txt'),(30,'upload/6_WG17Vx3.txt'),(31,'upload/6_f7K1FbL.txt'),(32,'upload/Exhaust_TkOOfBm.txt'),(33,'upload/Exhaust_0JFAMYk.txt');
/*!40000 ALTER TABLE `LinkData_uploadgenefile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add task result',7,'add_taskresult'),(26,'Can change task result',7,'change_taskresult'),(27,'Can delete task result',7,'delete_taskresult'),(28,'Can view task result',7,'view_taskresult'),(29,'Can add data collect',8,'add_datacollect'),(30,'Can change data collect',8,'change_datacollect'),(31,'Can delete data collect',8,'delete_datacollect'),(32,'Can view data collect',8,'view_datacollect'),(33,'Can add upload gene file',9,'add_uploadgenefile'),(34,'Can change upload gene file',9,'change_uploadgenefile'),(35,'Can delete upload gene file',9,'delete_uploadgenefile'),(36,'Can view upload gene file',9,'view_uploadgenefile');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_results_taskresult`
--

DROP TABLE IF EXISTS `django_celery_results_taskresult`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_celery_results_taskresult` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_id` varchar(255) NOT NULL,
  `status` varchar(50) NOT NULL,
  `content_type` varchar(128) NOT NULL,
  `content_encoding` varchar(64) NOT NULL,
  `result` longtext,
  `date_done` datetime(6) NOT NULL,
  `traceback` longtext,
  `meta` longtext,
  `task_args` longtext,
  `task_kwargs` longtext,
  `task_name` varchar(255) DEFAULT NULL,
  `worker` varchar(100) DEFAULT NULL,
  `date_created` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_id` (`task_id`),
  KEY `django_celery_results_taskresult_date_done_49edada6` (`date_done`),
  KEY `django_celery_results_taskresult_status_cbbed23a` (`status`),
  KEY `django_celery_results_taskresult_task_name_90987df3` (`task_name`),
  KEY `django_celery_results_taskresult_worker_f8711389` (`worker`),
  KEY `django_celery_results_taskresult_date_created_099f3424` (`date_created`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_results_taskresult`
--

LOCK TABLES `django_celery_results_taskresult` WRITE;
/*!40000 ALTER TABLE `django_celery_results_taskresult` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_results_taskresult` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(7,'django_celery_results','taskresult'),(8,'LinkData','datacollect'),(9,'LinkData','uploadgenefile'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'LinkData','0001_initial','2020-06-27 17:36:36.915172'),(2,'LinkData','0002_remove_datacollect_dataset_id','2020-06-27 17:36:36.960419'),(3,'LinkData','0003_datacollect_dataset_id','2020-06-27 17:36:36.994669'),(4,'LinkData','0004_auto_20200418_1852','2020-06-27 17:36:37.074298'),(5,'LinkData','0005_auto_20200419_2023','2020-06-27 17:36:37.100361'),(6,'LinkData','0006_uploadgenefile','2020-06-27 17:36:37.124504'),(7,'LinkData','0007_datacollect_celltype','2020-06-27 17:36:37.152609'),(8,'LinkData','0008_auto_20200603_2139','2020-06-27 17:36:37.184174'),(9,'LinkData','0009_datacollect_primary','2020-06-27 17:36:37.211810'),(10,'LinkData','0010_auto_20200625_1302','2020-06-27 17:36:37.216632'),(11,'contenttypes','0001_initial','2020-06-27 17:36:37.259297'),(12,'auth','0001_initial','2020-06-27 17:36:37.413328'),(13,'admin','0001_initial','2020-06-27 17:36:37.819646'),(14,'admin','0002_logentry_remove_auto_add','2020-06-27 17:36:37.930777'),(15,'admin','0003_logentry_add_action_flag_choices','2020-06-27 17:36:37.940546'),(16,'contenttypes','0002_remove_content_type_name','2020-06-27 17:36:38.025959'),(17,'auth','0002_alter_permission_name_max_length','2020-06-27 17:36:38.078901'),(18,'auth','0003_alter_user_email_max_length','2020-06-27 17:36:38.101486'),(19,'auth','0004_alter_user_username_opts','2020-06-27 17:36:38.110533'),(20,'auth','0005_alter_user_last_login_null','2020-06-27 17:36:38.156977'),(21,'auth','0006_require_contenttypes_0002','2020-06-27 17:36:38.166183'),(22,'auth','0007_alter_validators_add_error_messages','2020-06-27 17:36:38.175427'),(23,'auth','0008_alter_user_username_max_length','2020-06-27 17:36:38.232615'),(24,'auth','0009_alter_user_last_name_max_length','2020-06-27 17:36:38.294186'),(25,'auth','0010_alter_group_name_max_length','2020-06-27 17:36:38.312174'),(26,'auth','0011_update_proxy_permissions','2020-06-27 17:36:38.321797'),(27,'django_celery_results','0001_initial','2020-06-27 17:36:38.359052'),(28,'django_celery_results','0002_add_task_name_args_kwargs','2020-06-27 17:36:38.432049'),(29,'django_celery_results','0003_auto_20181106_1101','2020-06-27 17:36:38.437366'),(30,'django_celery_results','0004_auto_20190516_0412','2020-06-27 17:36:38.506992'),(31,'django_celery_results','0005_taskresult_worker','2020-06-27 17:36:38.530083'),(32,'django_celery_results','0006_taskresult_date_created','2020-06-27 17:36:38.587174'),(33,'django_celery_results','0007_remove_taskresult_hidden','2020-06-27 17:36:38.668922'),(34,'sessions','0001_initial','2020-06-27 17:36:38.693491'),(35,'LinkData','0011_auto_20200703_0603','2020-07-03 06:05:44.792322'),(36,'LinkData','0012_auto_20200703_0630','2020-07-03 06:31:02.065213');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-07-13  7:20:18
