from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators import csrf
from django.db.models import QuerySet
from LinkData.models import DataCollect, UploadGeneFile
# from RunLISA.models import RunInfo
from django.core.files import File
import os, time, datetime, sys
# from RunLISA.tasks import lisa
import json
from LinkData.tasks import GeneratePlotData, GenerateGeneList, GenerateHeatmapData, GenerateDotplotData, GenerateForm, GenerateViolinGridGeneData, ViolinGridGenePlot, GenerateGeneUMAPPlot, GenerateDiffgeneTable, GenerateViolinGridDatasetData, ViolinGridDatasetPlot, GenerateDotplotCPDBData
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def search_cancer(request):
    search_result = {}

    if request.POST:
        if request.POST['cancer'] == "All":
            search_result['datainfo'] = DataCollect.objects.all()
        else:
            search_result['datainfo'] = DataCollect.objects.filter(cancer__icontains=request.POST['cancer'])
        #ctx['datainfo'] = request.POST['cancer']
    else:
        search_result['datainfo'] = DataCollect.objects.all()

    return render(request, "dataset.html", search_result)

def doc(request):
    return render(request, "doc.html")

def statistics(request):
    return render(request, "statistics.html")

def select_dataset(request):
    search_result = {}

    class DataSet(object):
        """docstring for DataSet"""
        def __init__(self):
            self.file = ""
            self.umap = ""
            self.dataset_name = ""
            self.species = ""
            self.cancer = ""
            self.patient = 0
            self.cell = ""
            self.platform = ""
            self.publication = ""
            self.pmid = ""
            self.primary = ""
            self.treatment = ""
            self.treatment_detailed = ""
            self.column = 4

        def update(self, dataset = dict()):
            self.dataset_name = dataset["dataset_name"]
            self.species = dataset["species"]
            self.cancer = dataset["cancer"]
            if dataset["patient"] == 0:
                self.patient = "NA"
            else:
                self.patient = dataset["patient"]
            self.cell = f'{dataset["cell"]:,}'
            self.platform = dataset["platform"]
            self.publication = dataset["publication"]
            self.pmid = dataset["pmid"]
            self.primary = dataset["primary"]
            self.treatment = dataset["treatment"]
            self.treatment_detailed = dataset["treatment_detailed"]
            self.column = 4

    if request.POST:
        if request.is_ajax():
            if "dataset" in request.POST: 
                ## single dataset
                dataset = request.POST["dataset"]
                gene_file = os.path.join(BASE_DIR, "static/data/%s/%s_genes.tsv" %(dataset, dataset))
                umap_file = os.path.join(BASE_DIR, "static/data/%s/%s_umap.json" %(dataset, dataset))
                umap_dict = json.load(open(umap_file, "r"))
                celltype_list = sorted(list(set(umap_dict["Celltype_curated"])))
                # celltype_available = [(i,celltype_name_dict.get(i, i)) for i in celltype_list]
                # print(celltype_available)
                
                celltype_abbr_file = os.path.join(BASE_DIR, "static/commondata/Celltype_abbr.json")
                celltype_name_dict = json.load(open(celltype_abbr_file, "r"))
                celltype_abbr_list = [celltype_name_dict.get(i, i) for i in celltype_list]
                celltype_abbr_str = "<br>".join(celltype_abbr_list)

                umap_curated = "/static/data/%s/%s_umap_Celltype_curated.png" %(dataset, dataset)
                umap_cluster = "/static/data/%s/%s_umap_Cluster.png" %(dataset, dataset)
                diffgene_file = "/static/data/%s/%s_AllDiffGenes_table.json" %(dataset, dataset)
                gsea_kegg_up_cluster = "/static/data/%s/%s_cluster_DE_GSEA_kegg_UP_heatmap.png" %(dataset, dataset)
                gsea_kegg_down_cluster = "/static/data/%s/%s_cluster_DE_GSEA_kegg_DOWN_heatmap.png" %(dataset, dataset)
                gsea_hallmark_up_cluster = "/static/data/%s/%s_cluster_DE_GSEA_hallmark_UP_heatmap.png" %(dataset, dataset)
                gsea_hallmark_down_cluster = "/static/data/%s/%s_cluster_DE_GSEA_hallmark_DOWN_heatmap.png" %(dataset, dataset)
                gsea_meta_available = ["cluster"]

                for gsea_meta in ["Response", "Therapy", "Treatment"]:
                    if os.path.exists(os.path.join(BASE_DIR, "static/data/%s/%s_%s_DE_GSEA_kegg_UP_heatmap.png" %(dataset, dataset, gsea_meta))):
                        gsea_kegg_up_meta = "/static/data/%s/%s_%s_DE_GSEA_kegg_UP_heatmap.png" %(dataset, dataset, gsea_meta)
                        gsea_kegg_down_meta = "/static/data/%s/%s_%s_DE_GSEA_kegg_DOWN_heatmap.png" %(dataset, dataset, gsea_meta)
                        gsea_hallmark_up_meta = "/static/data/%s/%s_%s_DE_GSEA_hallmark_UP_heatmap.png" %(dataset, dataset, gsea_meta)
                        gsea_hallmark_down_meta = "/static/data/%s/%s_%s_DE_GSEA_hallmark_DOWN_heatmap.png" %(dataset, dataset, gsea_meta)
                        search_result["gsea_kegg_up_%s" %(gsea_meta)] = gsea_kegg_up_meta
                        search_result["gsea_kegg_down_%s" %(gsea_meta)] = gsea_kegg_down_meta
                        search_result["gsea_hallmark_up_%s" %(gsea_meta)] = gsea_hallmark_up_meta
                        search_result["gsea_hallmark_down_%s" %(gsea_meta)] = gsea_hallmark_down_meta
                        gsea_meta_available.append(gsea_meta)

                expr_mat = "/static/data/%s/%s_Expression.zip" %(dataset, dataset)
                de_table = "/static/data/%s/%s_AllDiffGenes_table.tsv" %(dataset, dataset)
                meta_info =  "/static/data/%s/%s_CellMetainfo_table.tsv" %(dataset, dataset)

                # CPDB
                # if len(celltype_list) < 5:
                #     cpdb_dotplot_celltype = celltype_list
                # else:
                #     cpdb_dotplot_celltype = celltype_list[:5]
                # print(cpdb_dotplot_celltype)
                # cpdb_dotplot_file = GenerateDotplotCPDBData(dataset = dataset, gene_pairs_rank = 0.05, cell_list = cpdb_dotplot_celltype)
                

                genes = open(gene_file, "r").readlines()
                genes = [i.strip() for i in genes]
                genes.sort()

                res_forms = GenerateForm(dataset)
                # search_result["cluster_form"] = res_forms["cluster_form"]
                search_result["annotation_form"] = res_forms["annotation_form"]
                search_result["comparison_form"] = res_forms["comparison_form"]
                search_result["group_form"] = res_forms["group_form"]
                search_result["available_genes"] = genes
                search_result["umap_anno"] = umap_curated
                search_result["umap_cluster"] = umap_cluster
                search_result["diffgene_file"] = diffgene_file
                search_result["celltype_abbr_str"] = celltype_abbr_str
                search_result["gsea_kegg_up_cluster"] = gsea_kegg_up_cluster
                search_result["gsea_kegg_down_cluster"] = gsea_kegg_down_cluster
                search_result["gsea_hallmark_up_cluster"] = gsea_hallmark_up_cluster
                search_result["gsea_hallmark_down_cluster"] = gsea_hallmark_down_cluster
                search_result["expr_mat"] = expr_mat
                search_result["de_table"] = de_table
                search_result["meta_info"] = meta_info
                # search_result["celltype_available"] = celltype_available
                search_result["gsea_meta_available"] = gsea_meta_available
                # search_result["celltype_selected"] = cpdb_dotplot_celltype
                # search_result["cpdb_dotplot_file"] = cpdb_dotplot_file
                search_result["current_dataset"] = dataset

                return HttpResponse(json.dumps(search_result), content_type='application/json')


            if "dataset_selected[]" not in request.POST:
                dataset = request.POST["dataset_selected"]
                ## search gene in single dataset
                if "genesearch[]" in request.POST:
                    gene_list = request.POST.getlist("genesearch[]")
                    print(gene_list)
                    print(dataset)
                    print(request.POST["plottype"])
                    if request.POST["plottype"] == "umap":
                        time.sleep(1)
                        gene_umapplot_list = []
                        for gene in gene_list:
                            if os.path.exists(os.path.join(BASE_DIR, "static/data/%s/Gene/%s_%s_umap.png" %(dataset, dataset, gene))):
                                gene_umapplot_file = "/static/data/%s/Gene/%s_%s_umap.png" %(dataset, dataset, gene)
                            else:
                                gene_umapplot_file = GenerateGeneUMAPPlot(dataset, gene, gene_label = gene)
                            gene_umapplot_list.append(gene_umapplot_file)
                        search_result["gene_umap"] = gene_umapplot_list
                    if request.POST["plottype"] == "violin":
                        annotation_level = request.POST["annotation"]
                        groupby = request.POST["group"]
                        time.sleep(2)
                        if groupby == "None":
                            violin_plot = ViolinGridDatasetPlot(GenerateViolinGridDatasetData(dataset, gene_list, annotation_level), dataset,annotation_level, groupby)
                            search_result["violin_plot"] = violin_plot
                        else:
                            violin_plot = ViolinGridDatasetPlot(GenerateViolinGridDatasetData(dataset, gene_list, [annotation_level, groupby]), dataset, annotation_level, groupby)
                            search_result["violin_plot"] = violin_plot

                        

                    # gene = request.POST["genesearch"]
                    # # res_files = GeneratePlotData(dataset, gene)
                    # search_result['selected_gene'] = gene
                    # search_result["violin_file"] = res_files["violin"]
                    # search_result["gene_umap_overview_file"] = umap_file_return
                    # search_result["gene_umap_distribution_file"] = res_files["gene_umap"]
                    # search_result['gene_umap_label'] = "Expression"

                if request.FILES.get('genelistfile', None):
                    print(request.POST)
                    ## upload gene signature in single dataset
                    print(dataset)

                    collapse_mode = request.POST["collapsemode"]
                    gene_label = request.POST["genelistlabel"]
                    upgene_file = request.FILES.get('genelistfile', None)
                    UploadGeneFile.objects.create(genefile = upgene_file)
                    newrecord = UploadGeneFile.objects.order_by("id").last()

                    upgene_file = os.path.join(BASE_DIR, "media/") + str(newrecord.genefile)
                    upgene_list = open(upgene_file, "r").readlines()
                    upgene_list = [i.strip() for i in upgene_list]
                    upgene_list = list(set(upgene_list))
                # if "genelist" in request.POST:
                #     upgene_list = request.POST["genelist"].split("\n")
                #     upgene_list = list(set(upgene_list))
                #     collapse_mode = request.POST["collapsemode"]
                #     gene_label = request.POST["genelistlabel"]
                #     print(upgene_list)

                    if request.POST["plottype"] == "umap":
                        time.sleep(1)
                        gene_umapplot_list = []
                        gene_umapplot_file = GenerateGeneUMAPPlot(dataset, upgene_list, gene_label, collapse_mode)
                        gene_umapplot_list.append(gene_umapplot_file)
                        search_result["gene_umap"] = gene_umapplot_list

                    if request.POST["plottype"] == "violin":
                        gene_label_list = [gene_label]
                        # violin_plot = ViolinGridDatasetPlot(GenerateViolinGridDatasetData(dataset, upgene_list, annotation_level, gene_label_list, collapse_mode), dataset)
                        # search_result["violin_plot"] = violin_plot
                        annotation_level = request.POST["annotation"]
                        groupby = request.POST["group"]
                        time.sleep(2)
                        if groupby == "None":
                            violin_plot = ViolinGridDatasetPlot(GenerateViolinGridDatasetData(dataset, upgene_list, annotation_level, gene_label_list, collapse_mode), dataset, annotation_level, groupby)
                            search_result["violin_plot"] = violin_plot
                        else:
                            violin_plot = ViolinGridDatasetPlot(GenerateViolinGridDatasetData(dataset, upgene_list, [annotation_level, groupby], gene_label_list, collapse_mode), dataset, annotation_level, groupby)
                            search_result["violin_plot"] = violin_plot

                # if "celltype_selected[]" in request.POST:
                #     cpdb_dotplot_celltype = request.POST.getlist("celltype_selected[]")
                #     rank = request.POST["rank"]
                #     cpdb_dotplot_file = GenerateDotplotCPDBData(dataset = dataset, gene_pairs_rank = float(rank), cell_list = cpdb_dotplot_celltype)
                #     search_result["cpdb_dotplot_file"] = cpdb_dotplot_file

                return HttpResponse(json.dumps(search_result), content_type='application/json')

            else:
                if "genesearch[]" not in request.POST and "genelistfile" not in request.FILES:
                    # submit multiple datasets
                    print(request.POST)
                    dataset_list = request.POST.getlist("dataset_selected[]")
                    print(dataset_list)
                    if len(dataset_list) > 1:
                        gene_file_list = [os.path.join(BASE_DIR, "static/data/%s/%s_genes.tsv" %(dataset, dataset)) for dataset in dataset_list]

                        available_genes = []
                        for gene_file in gene_file_list:
                            genes = open(gene_file, "r").readlines()
                            genes = [i.strip() for i in genes]
                            available_genes = available_genes + genes
                        available_genes = sorted(list(set(available_genes)))

                        dataset_return_list = []
                        for dataset in dataset_list:
                            data = {}
                            data["umap"] = "/static/data/%s/%s_umap_Celltype_curated.png" %(dataset, dataset)
                            data["dataset_name"] = dataset
                            dataset_return_list.append(data)

                        search_result["dataset_list"] = dataset_return_list
                        search_result["available_genes"] = available_genes
                        search_result["dataset_select"] = dataset_list
                        return HttpResponse(json.dumps(search_result), content_type='application/json')

                else:
                    gene_umapplot_list = []
                    dataset_list = request.POST.getlist("dataset_selected[]")
                    human_mouse_gene_match_file = os.path.join(BASE_DIR, "static/commondata/Human_mouse_gene.json")
                    mouse_human_gene_match_file = os.path.join(BASE_DIR, "static/commondata/Mouse_human_gene.json")
                    human_mouse_gene_dict = json.load(open(human_mouse_gene_match_file, "r"))
                    mouse_human_gene_dict = json.load(open(mouse_human_gene_match_file, "r"))
                    # search gene in multiple datasets
                    if "genesearch[]" in request.POST:
                        gene_list = request.POST.getlist("genesearch[]")
                        gene_list_human = []
                        gene_list_mouse = []
                        for gene in gene_list:
                            if gene.isupper():
                                gene_list_human.append(gene)
                                gene_list_mouse.append(human_mouse_gene_dict.get(gene, gene))
                            else:
                                gene_list_mouse.append(gene)
                                gene_list_human.append(mouse_human_gene_dict.get(gene, gene))
                        for dataset in dataset_list:
                            dataset_species = DataCollect.objects.get(dataset_name = dataset).species
                            if dataset_species == "Mouse":
                                gene_list_species = gene_list_mouse
                            else:
                                gene_list_species = gene_list_human
                            dataset_gene_umappplot_list = []
                            for gene in gene_list_species:
                                if os.path.exists(os.path.join(BASE_DIR, "static/data/%s/Gene/%s_%s_umap.png" %(dataset, dataset, gene))):
                                    gene_umapplot_file = "/static/data/%s/Gene/%s_%s_umap.png" %(dataset, dataset, gene)
                                else:
                                    gene_umapplot_file = GenerateGeneUMAPPlot(dataset, gene, gene_label = gene)
                                dataset_gene_umappplot_list.append(gene_umapplot_file)
                            gene_umapplot_list.append(dataset_gene_umappplot_list)

                    # upload gene signature in multiple datasets
                    if request.FILES.get('genelistfile', None):
                        collapse_mode = request.POST["collapsemode"]
                        gene_label = request.POST["genelistlabel"]
                        upgene_file = request.FILES.get('genelistfile', None)
                        UploadGeneFile.objects.create(genefile = upgene_file)
                        newrecord = UploadGeneFile.objects.order_by("id").last()

                        upgene_file = os.path.join(BASE_DIR, "media/") + str(newrecord.genefile)
                        upgene_list = open(upgene_file, "r").readlines()
                        upgene_list = [i.strip() for i in upgene_list]
                        upgene_list = list(set(upgene_list))
                        print(upgene_list)
                        gene_list_human = []
                        gene_list_mouse = []
                        for gene in upgene_list:
                            if gene.isupper():
                                gene_list_human.append(gene)
                                gene_list_mouse.append(human_mouse_gene_dict.get(gene, gene))
                            else:
                                gene_list_mouse.append(gene)
                                gene_list_human.append(mouse_human_gene_dict.get(gene, gene))
                        for dataset in dataset_list:
                            dataset_species = DataCollect.objects.get(dataset_name = dataset).species
                            if dataset_species == "Mouse":
                                gene_list_species = gene_list_mouse
                            else:
                                gene_list_species = gene_list_human
                            gene_umapplot_file = GenerateGeneUMAPPlot(dataset, gene_list_species, gene_label, collapse_mode)
                            gene_umapplot_list.append(gene_umapplot_file)

                    search_result["gene_umap"] = gene_umapplot_list
                    print(gene_umapplot_list)
                    return HttpResponse(json.dumps(search_result), content_type='application/json')

        else:
            # submit dataset
            dataset_list = request.POST.getlist("dataset_checkbox_list")
            if len(dataset_list) > 1:
                gene_file_list = [os.path.join(BASE_DIR, "static/data/%s/%s_genes.tsv" %(dataset, dataset)) for dataset in dataset_list]

                available_genes = []
                for gene_file in gene_file_list:
                    genes = open(gene_file, "r").readlines()
                    genes = [i.strip() for i in genes]
                    available_genes = available_genes + genes
                available_genes = sorted(list(set(available_genes)))

                dataset_return_list = []
                for dataset in dataset_list:
                    data = DataSet()
                    data.umap = "/static/data/%s/%s_umap_Celltype_curated.png" %(dataset, dataset)
                    data.file = "/static/data/%s/%s_Data.zip" %(dataset, dataset)
                    data.dataset_name = dataset
                    dataset_return_list.append(data)

                search_result["dataset_list"] = dataset_return_list
                search_result["available_genes"] = available_genes
                search_result["dataset_select"] = dataset_list
                return render(request, "gallery_gene.html", search_result)

            if len(dataset_list) == 1:
                return redirect("/data/%s" %(dataset_list[0]))

    else:
        # search datasets according to cancer type, cell type and species
        print(request.GET)
        if request.GET:
            cancer_list = []
            celltype_list = []
            species_list = []
            treatment_list = []
            primary_list = []
            query_result_cancer = DataCollect.objects.exclude(species__in = ["Human","Mouse"])
            query_result_celltype = DataCollect.objects.exclude(species__in = ["Human","Mouse"])
            query_result_treatment = DataCollect.objects.exclude(species__in = ["Human","Mouse"])
            query_result_primary = DataCollect.objects.exclude(species__in = ["Human","Mouse"])
            if "cancer" in request.GET:
                cancer_list = request.GET.getlist('cancer')
                for cancer in cancer_list:
                    query_result = DataCollect.objects.filter(cancer__icontains=cancer)
                    query_result_cancer = query_result_cancer | query_result
                search_result['cancerlist'] = cancer_list
            else:
                query_result_cancer = DataCollect.objects.all()
                search_result['cancerlist'] = [""]

            if "celltype" in request.GET:
                celltype_list = request.GET.getlist('celltype')
                for celltype in celltype_list:
                    query_result = DataCollect.objects.filter(celltype__icontains=celltype)
                    query_result_celltype = query_result_celltype | query_result
                search_result['celltypelist'] = celltype_list
            else:
                query_result_celltype = DataCollect.objects.all()
                search_result['celltypelist'] = [""]

            if "species" in request.GET and request.GET["species"] != "":
                species_list = [request.GET["species"]]
            else:
                species_list = ["Human", "Mouse"]
            search_result['specieslist'] = species_list
            query_result_species = DataCollect.objects.filter(species__in=species_list)

            if "treatment" in request.GET:
                treatment_list = request.GET.getlist('treatment')
                for treatment in treatment_list:
                    query_result = DataCollect.objects.filter(treatment__icontains=treatment)
                    query_result_treatment = query_result_treatment | query_result
                search_result['treatmentlist'] = treatment_list
            else:
                query_result_treatment = DataCollect.objects.all()
                search_result['treatmentlist'] = [""]

            if "primary" in request.GET:
                primary_list = request.GET.getlist('primary')
                for primary in primary_list:
                    query_result = DataCollect.objects.filter(primary__icontains=primary)
                    query_result_primary = query_result_primary | query_result
                search_result['primarylist'] = primary_list
            else:
                query_result_primary = DataCollect.objects.all()
                search_result['primarylist'] = [""]

            # print(query_result_treatment)

            query_result_final = (((query_result_cancer & query_result_celltype) & query_result_species) & query_result_treatment) & query_result_primary
            print(query_result_final)
            query_result_list = list(query_result_final)

        else:
            query_result = DataCollect.objects.all()
            query_result_list = list(query_result)
            search_result['cancerlist'] = [""]
            search_result['celltypelist'] = [""]
            species_list = ["Human", "Mouse"]
            search_result['specieslist'] = species_list
            search_result['treatmentlist'] = [""]
            search_result['primarylist'] = [""]

        query_result_list = [i.__dict__ for i in query_result_list]
        data_list = []
        for i in range(len(query_result_list)):
            data = DataSet()
            data.update(query_result_list[i])
            data.column = i%3 +1
            data.umap = "/static/data/%s/%s_umap.png" %(data.dataset_name, data.dataset_name)
            data.file = "/static/data/%s/%s_Data.zip" %(data.dataset_name, data.dataset_name)
            data_list.append(data)            

        # if data_list[len(data_list)-1].column == 1:
        #     data_list[len(data_list)-1].column = 4
        # elif data_list[len(data_list)-1].column == 2:
        #     data_list[len(data_list)-1].column = 3
        search_result['datainfo'] = data_list

        query_all = DataCollect.objects.all()
        query_all_list = list(query_all)
        search_result['searchinfo'] = "Return %s across %s datasets" %(len(data_list), len(query_all_list))

        return render(request, "gallery.html", search_result)

def search_gene(request):
    search_result = {}
    all_datasets = [data.dataset_name for data in DataCollect.objects.all()]
    all_datasets_dict = defaultdict(list)
    for data in DataCollect.objects.all():
        cancer_type = data.cancer.split(" (")[0]
        for i in cancer_type.split(", "):
            all_datasets_dict[i].append(data.dataset_name)
    # print(dict(all_datasets_dict))
    gene_list = GenerateGeneList(all_datasets)
    print(request.GET)
    if request.POST:
        if request.is_ajax():
            print(request.POST)
            if "plottype" in request.POST:
                if "dataset[]" in request.POST:
                    datasets = request.POST.getlist('dataset[]')
                else:
                    if "cancer[]" in request.POST and "All" not in request.POST.getlist('cancer[]'):
                        query_result = DataCollect.objects.filter(cancer__in=request.POST.getlist('cancer[]'))
                    else:
                        query_result = DataCollect.objects.all()
                    datasets = [data.dataset_name for data in query_result]
                gene = request.POST["genesearch"]
                annotation_level = request.POST["annotation"]
                if request.POST["plottype"] == "heatmap":
                    search_result['heatmap_file'] = GenerateHeatmapData(datasets, gene, annotation_level)
                if request.POST["plottype"] == "violin":
                    violin_plot = ViolinGridGenePlot(GenerateViolinGridGeneData(datasets, gene, annotation_level), gene)
                    search_result["violin_svg"] = violin_plot[0]
                    search_result["violin_pdf"] = violin_plot[1]
                search_result['selected_gene'] = gene
                search_result["available_genes"] = gene_list
                # search_result["violin_svg"] = ViolinGridPlot(GenerateViolinGridData(all_datasets, gene), gene)
                return HttpResponse(json.dumps(search_result), content_type='application/json')
            else:
                query_result_cancer = DataCollect.objects.exclude(species__in = ["Human","Mouse"])
                query_result_celltype = DataCollect.objects.exclude(species__in = ["Human","Mouse"])
                if "cancer[]" in request.POST and "All" not in request.POST.getlist('cancer[]'):
                    cancer_list = request.POST.getlist('cancer[]')
                    for cancer in cancer_list:
                        query_result = DataCollect.objects.filter(cancer__icontains=cancer)
                        query_result_cancer = query_result_cancer | query_result
                else:
                    query_result_cancer = DataCollect.objects.all()

                if "celltype[]" in request.POST:
                    celltype_list = request.POST.getlist('celltype[]')
                    for celltype in celltype_list:
                        query_result = DataCollect.objects.filter(celltype__icontains=celltype)
                        query_result_celltype = query_result_celltype | query_result
                else:
                    query_result_celltype = DataCollect.objects.all()

                query_result_final = query_result_cancer & query_result_celltype
                datasets = [data.dataset_name for data in query_result_final]
                search_result["datasets"] = datasets
                print(datasets)
                return HttpResponse(json.dumps(search_result), content_type='application/json')


        # else:
        #     query_result = DataCollect.objects.all()
        #     datasets = [data.dataset_name for data in query_result]
        #     gene = request.POST["genesearch"]
        #     annotation_level = "Celltype_curated"
        #     search_result['heatmap_file'] = GenerateHeatmapData(datasets, gene, annotation_level)
        #     search_result['selected_gene'] = gene
        #     search_result["available_genes"] = gene_list

        #     return render(request, "gene.html", search_result)

    else:
        if "genesearch" in request.GET:
            # query_result = DataCollect.objects.all()
            # datasets = [data.dataset_name for data in query_result]
            gene = request.GET["genesearch"]
            annotation_level = "Celltype_curated"
            # search_result['heatmap_file'] = GenerateHeatmapData(datasets, gene, annotation_level)
            search_result['selected_cancer'] = "BRCA"
            search_result['selected_gene'] = gene
            search_result["available_genes"] = gene_list
            search_result["available_cancer_dict"] = dict(all_datasets_dict)

            return render(request, "gene.html", search_result)
        else:
            search_result["available_genes"] = gene_list
            search_result["available_cancer_dict"] = dict(all_datasets_dict)
            return render(request, "gene.html", search_result)

        # if request.POST:
        #     search_result['explisa'] = ExpLISA.objects.filter(tf=request.POST['tf'])
        # return render(request, "gene.html", search_result)


def home(request):
    search_result = {}
    all_datasets = [data.dataset_name for data in DataCollect.objects.all()]
    gene_list = GenerateGeneList(all_datasets)
    if request.POST:
        gene = request.POST["genesearch"]
        return redirect("/search-gene/?genesearch=%s" %(gene))
    else:
        search_result["available_genes"] = gene_list
        return render(request,'index.html', search_result)

# def data(request, dataset):
#     gene_file = "./static/data/%s/%s_genes.tsv" %(dataset, dataset)
#     umap_file_return = "/data/%s/%s_umap.json" %(dataset, dataset)

#     genes = open(gene_file, "r").readlines()
#     genes = [i.strip() for i in genes]
#     genes.sort()

#     search_result = {}
#     if request.method == "POST":
#         if "genesearch" in request.POST:
#             gene = request.POST["genesearch"]
#             res_files = GeneratePlotData(dataset, gene)
#             search_result['selected_gene'] = gene
#             search_result["violin_file"] = res_files["violin"]
#             search_result["gene_umap_overview_file"] = umap_file_return
#             search_result["gene_umap_distribution_file"] = res_files["gene_umap"]
#             search_result['gene_umap_label'] = "Expression"

#         if request.FILES.get('genelistfile', None):
#             collapse_mode = request.POST["collapsemode"]
#             upgene_file = request.FILES.get('genelistfile', None)
#             UploadGeneFile.objects.create(genefile = upgene_file)
#             newrecord = UploadGeneFile.objects.order_by("id").last()
#             upgene_file = "./media/" + str(newrecord.genefile)
#             upgene_list = open(upgene_file, "r").readlines()
#             upgene_list = [i.strip() for i in upgene_list]

#             upgene_list = list(set(genes) & set(upgene_list))

#             search_result["gene_dot_file"] = GenerateDotplotData(dataset, upgene_list)
#             res_files = GeneratePlotData(dataset, upgene_list, collapse_mode)
#             search_result["violin_file"] = res_files["violin"]
#             search_result["gene_umap_overview_file"] = umap_file_return
#             search_result["gene_umap_distribution_file"] = res_files["gene_umap"]
#             if collapse_mode == "mean":
#                 search_result['gene_umap_label'] = "Mean expression"
#                 search_result['selected_gene'] = "Custom gene list (collapsed by mean)"
#             if collapse_mode == "median":
#                 search_result['gene_umap_label'] = "Median expression"
#                 search_result['selected_gene'] = "Custom gene list (collapsed by median)"

#     # form_render_list = GroupedExpenseForm().as_p()
#     # print(GroupedExpenseForm())

#     res_forms = GenerateForm(dataset)
#     search_result["cluster_form"] = res_forms["cluster_form"]
#     search_result["annotation_form"] = res_forms["annotation_form"]
#     search_result["comparison_form"] = res_forms["comparison_form"]
#     search_result["group_form"] = res_forms["group_form"]
#     search_result["available_genes"] = genes
#     search_result["umap_file"] = umap_file_return
#     search_result["current_dataset"] = dataset

#     return render(request,'dataset_gene_0.html', search_result)

def data(request, dataset):
    # if dataset:
    #     pass
    # else:
    #     dataset = request.POST["dataset_selected"]
    # print(dataset)

    # celltype_name_dict = {"B": "B (B cells)",
    # "CD4Tconv": "CD4Tconv (Conventional CD4 T cells)",
    # "CD8T": "CD8T (CD8 T cells)",
    # "CD8Tex": "CD8Tex (Exhausted CD8 T cells)",
    # "DC": "DC (Dendritic cells)",
    # "Endothelial": "Endothelial (Endothelial cells)",
    # "Fibroblasts": "Fibroblasts",
    # "ILC": "ILC (Innate lymphoid cells)",
    # "Malignant": "Malignant (Malignant cells)",
    # "Mast": "Mast (Mast cells)",
    # "Mono/Macro": "Mono/Macro (Monocytes or macrophages)",
    # "Myofibroblasts": "Myofibroblasts",
    # "NK": "NK (Natural killer cells)",
    # "Neutrophils": "Neutrophils",
    # "pDC": "pDC (Plasmacytoid dendritic cells)",
    # "Plasma": "Plasma (Plasma cells)",
    # "TMKI67": "TMKI67 (Proliferating T cells)",
    # "Treg": "Treg (Regulatory T cells)"}
    celltype_abbr_file = os.path.join(BASE_DIR, "static/commondata/Celltype_abbr.json")
    celltype_name_dict = json.load(open(celltype_abbr_file, "r"))

    print(request.is_ajax())
    search_result = {}
    
    # sys.stdout = open(os.path.join(BASE_DIR, "log/script.log"), 'a')

    if request.method == "POST":
        if request.is_ajax():
            print(request.POST)
            if "genesearch[]" in request.POST:
                gene_list = request.POST.getlist("genesearch[]")
                print(gene_list)
                print(dataset)
                print(request.POST["plottype"])
                if request.POST["plottype"] == "umap":
                    gene_umapplot_list = []
                    for gene in gene_list:
                        if os.path.exists(os.path.join(BASE_DIR, "static/data/%s/Gene/%s_%s_umap.png" %(dataset, dataset, gene))):
                            gene_umapplot_file = "/static/data/%s/Gene/%s_%s_umap.png" %(dataset, dataset, gene)
                        else:
                            gene_umapplot_file = GenerateGeneUMAPPlot(dataset, gene, gene_label = gene)
                        gene_umapplot_list.append(gene_umapplot_file)
                    search_result["gene_umap"] = gene_umapplot_list
                if request.POST["plottype"] == "violin":
                    annotation_level = request.POST["annotation"]
                    groupby = request.POST["group"]
                    time.sleep(2)
                    if groupby == "None":
                        violin_plot = ViolinGridDatasetPlot(GenerateViolinGridDatasetData(dataset, gene_list, annotation_level), dataset,annotation_level, groupby)
                        search_result["violin_plot"] = violin_plot
                    else:
                        violin_plot = ViolinGridDatasetPlot(GenerateViolinGridDatasetData(dataset, gene_list, [annotation_level, groupby]), dataset, annotation_level, groupby)
                        search_result["violin_plot"] = violin_plot

                    

                # gene = request.POST["genesearch"]
                # # res_files = GeneratePlotData(dataset, gene)
                # search_result['selected_gene'] = gene
                # search_result["violin_file"] = res_files["violin"]
                # search_result["gene_umap_overview_file"] = umap_file_return
                # search_result["gene_umap_distribution_file"] = res_files["gene_umap"]
                # search_result['gene_umap_label'] = "Expression"

            if request.FILES.get('genelistfile', None):
                print(dataset)

                collapse_mode = request.POST["collapsemode"]
                gene_label = request.POST["genelistlabel"]
                upgene_file = request.FILES.get('genelistfile', None)
                UploadGeneFile.objects.create(genefile = upgene_file)
                newrecord = UploadGeneFile.objects.order_by("id").last()

                upgene_file = os.path.join(BASE_DIR, "media/") + str(newrecord.genefile)
                upgene_list = open(upgene_file, "r").readlines()
                upgene_list = [i.strip() for i in upgene_list]
                upgene_list = list(set(upgene_list))
            # if "genelist" in request.POST:
            #     upgene_list = request.POST["genelist"].split("\n")
            #     upgene_list = list(set(upgene_list))
            #     collapse_mode = request.POST["collapsemode"]
            #     gene_label = request.POST["genelistlabel"]
            #     print(upgene_list)

                if request.POST["plottype"] == "umap":
                    gene_umapplot_list = []
                    gene_umapplot_file = GenerateGeneUMAPPlot(dataset, upgene_list, gene_label, collapse_mode)
                    gene_umapplot_list.append(gene_umapplot_file)
                    search_result["gene_umap"] = gene_umapplot_list

                if request.POST["plottype"] == "violin":
                    gene_label_list = [gene_label]
                    # violin_plot = ViolinGridDatasetPlot(GenerateViolinGridDatasetData(dataset, upgene_list, annotation_level, gene_label_list, collapse_mode), dataset)
                    # search_result["violin_plot"] = violin_plot
                    annotation_level = request.POST["annotation"]
                    groupby = request.POST["group"]
                    time.sleep(2)
                    if groupby == "None":
                        violin_plot = ViolinGridDatasetPlot(GenerateViolinGridDatasetData(dataset, upgene_list, annotation_level, gene_label_list, collapse_mode), dataset, annotation_level, groupby)
                        search_result["violin_plot"] = violin_plot
                    else:
                        violin_plot = ViolinGridDatasetPlot(GenerateViolinGridDatasetData(dataset, upgene_list, [annotation_level, groupby], gene_label_list, collapse_mode), dataset, annotation_level, groupby)
                        search_result["violin_plot"] = violin_plot

            # if "celltype_selected[]" in request.POST:
            #     cpdb_dotplot_celltype = request.POST.getlist("celltype_selected[]")
            #     rank = request.POST["rank"]
            #     cpdb_dotplot_file = GenerateDotplotCPDBData(dataset = dataset, gene_pairs_rank = float(rank), cell_list = cpdb_dotplot_celltype)
            #     search_result["cpdb_dotplot_file"] = cpdb_dotplot_file

            return HttpResponse(json.dumps(search_result), content_type='application/json')

    # form_render_list = GroupedExpenseForm().as_p()
    # print(GroupedExpenseForm())
    else:
        if dataset != "undefined":
            gene_file = os.path.join(BASE_DIR, "static/data/%s/%s_genes.tsv" %(dataset, dataset))
            umap_file = os.path.join(BASE_DIR, "static/data/%s/%s_umap.json" %(dataset, dataset))
            umap_dict = json.load(open(umap_file, "r"))
            celltype_list = sorted(list(set(umap_dict["Celltype_curated"])))
            # celltype_available = [(i,celltype_name_dict.get(i, i)) for i in celltype_list]
            # print(celltype_available)
            
            celltype_abbr_list = [celltype_name_dict.get(i, i) for i in celltype_list]
            celltype_abbr_str = "<br>".join(celltype_abbr_list)

            umap_curated = "/static/data/%s/%s_umap_Celltype_curated.png" %(dataset, dataset)
            umap_cluster = "/static/data/%s/%s_umap_Cluster.png" %(dataset, dataset)
            diffgene_file = "/static/data/%s/%s_AllDiffGenes_table.json" %(dataset, dataset)
            gsea_kegg_up_cluster = "/static/data/%s/%s_cluster_DE_GSEA_kegg_UP_heatmap.png" %(dataset, dataset)
            gsea_kegg_down_cluster = "/static/data/%s/%s_cluster_DE_GSEA_kegg_DOWN_heatmap.png" %(dataset, dataset)
            gsea_hallmark_up_cluster = "/static/data/%s/%s_cluster_DE_GSEA_hallmark_UP_heatmap.png" %(dataset, dataset)
            gsea_hallmark_down_cluster = "/static/data/%s/%s_cluster_DE_GSEA_hallmark_DOWN_heatmap.png" %(dataset, dataset)
            gsea_meta_available = ["cluster"]

            for gsea_meta in ["Response", "Therapy", "Treatment"]:
                if os.path.exists(os.path.join(BASE_DIR, "static/data/%s/%s_%s_DE_GSEA_kegg_UP_heatmap.png" %(dataset, dataset, gsea_meta))):
                    gsea_kegg_up_meta = "/static/data/%s/%s_%s_DE_GSEA_kegg_UP_heatmap.png" %(dataset, dataset, gsea_meta)
                    gsea_kegg_down_meta = "/static/data/%s/%s_%s_DE_GSEA_kegg_DOWN_heatmap.png" %(dataset, dataset, gsea_meta)
                    gsea_hallmark_up_meta = "/static/data/%s/%s_%s_DE_GSEA_hallmark_UP_heatmap.png" %(dataset, dataset, gsea_meta)
                    gsea_hallmark_down_meta = "/static/data/%s/%s_%s_DE_GSEA_hallmark_DOWN_heatmap.png" %(dataset, dataset, gsea_meta)
                    search_result["gsea_kegg_up_%s" %(gsea_meta)] = gsea_kegg_up_meta
                    search_result["gsea_kegg_down_%s" %(gsea_meta)] = gsea_kegg_down_meta
                    search_result["gsea_hallmark_up_%s" %(gsea_meta)] = gsea_hallmark_up_meta
                    search_result["gsea_hallmark_down_%s" %(gsea_meta)] = gsea_hallmark_down_meta
                    gsea_meta_available.append(gsea_meta)

            expr_mat = "/static/data/%s/%s_Expression.zip" %(dataset, dataset)
            de_table = "/static/data/%s/%s_AllDiffGenes_table.tsv" %(dataset, dataset)
            meta_info =  "/static/data/%s/%s_CellMetainfo_table.tsv" %(dataset, dataset)


            # CPDB
            # if len(celltype_list) < 5:
            #     cpdb_dotplot_celltype = celltype_list
            # else:
            #     cpdb_dotplot_celltype = celltype_list[:5]
            # print(cpdb_dotplot_celltype)
            # cpdb_dotplot_file = GenerateDotplotCPDBData(dataset = dataset, gene_pairs_rank = 0.05, cell_list = cpdb_dotplot_celltype)
            

            genes = open(gene_file, "r").readlines()
            genes = [i.strip() for i in genes]
            genes.sort()

            res_forms = GenerateForm(dataset)
            # search_result["cluster_form"] = res_forms["cluster_form"]
            search_result["annotation_form"] = res_forms["annotation_form"]
            search_result["comparison_form"] = res_forms["comparison_form"]
            search_result["group_form"] = res_forms["group_form"]
            search_result["available_genes"] = genes
            search_result["umap_anno"] = umap_curated
            search_result["umap_cluster"] = umap_cluster
            search_result["diffgene_file"] = diffgene_file
            search_result["celltype_abbr_str"] = celltype_abbr_str
            search_result["gsea_kegg_up_cluster"] = gsea_kegg_up_cluster
            search_result["gsea_kegg_down_cluster"] = gsea_kegg_down_cluster
            search_result["gsea_hallmark_up_cluster"] = gsea_hallmark_up_cluster
            search_result["gsea_hallmark_down_cluster"] = gsea_hallmark_down_cluster
            search_result["expr_mat"] = expr_mat
            search_result["de_table"] = de_table
            search_result["meta_info"] = meta_info
            # search_result["celltype_available"] = celltype_available
            search_result["gsea_meta_available"] = gsea_meta_available
            # search_result["celltype_selected"] = cpdb_dotplot_celltype
            # search_result["cpdb_dotplot_file"] = cpdb_dotplot_file
            search_result["current_dataset"] = dataset

            return render(request,'dataset_gene.html', search_result)
        else:
            return HttpResponse()

