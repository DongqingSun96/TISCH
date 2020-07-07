from django.db import models

# Create your models here.
class DataCollect(models.Model):
    dataset_type_choice = [('TME','TME'), ('ICB', 'ICB'), ('Normal', 'Normal')]
    species_choice = [('Human', 'Human'), ('Mouse', 'Mouse')]

    dataset_name = models.CharField(max_length = 100, db_column = 'Dataset Name', primary_key = True)
    dataset_id = models.CharField(max_length = 50, db_column = 'Dataset ID')
    dataset_type = models.CharField(max_length = 20, db_column = 'Dataset Type', choices = dataset_type_choice, default = "TME")
    treatment = models.CharField(max_length = 50, db_column = 'Treatment', default = "None")
    treatment_detailed = models.CharField(max_length = 50, db_column = 'Detailed Treatment', default = "None")
    species = models.CharField(max_length = 20, db_column = 'Species', choices = species_choice, default = "Human")
    cancer = models.CharField(max_length = 50, db_column = 'Cancer Type')
    celltype = models.CharField(max_length = 1000, db_column = 'Cell Type', default = "None")
    primary = models.CharField(max_length = 50, db_column = 'Primary', default = "None")
    platform = models.CharField(max_length = 50, db_column = 'Platform')
    patient = models.IntegerField(db_column = 'Patient Number', null = True)
    cell = models.IntegerField(db_column = 'Cell Number')
    publication = models.CharField(max_length = 100, db_column = 'Publication')
    pmid = models.CharField(max_length = 20, db_column = 'PMID')

# class ExpLISA(models.Model):
#     dataset = models.CharField(max_length = 50, db_column = 'Dataset ID')
#     cancer = models.CharField(max_length = 50, db_column = 'Cancer Type')
#     subcluster = models.CharField(max_length = 50, db_column = 'Subcluster')
#     tf = models.CharField(max_length = 20, db_column = 'Transcription Factor')
#     expression = models.DecimalField(max_digits = 5, decimal_places = 2, db_column = 'Expression')
#     regscore = models.DecimalField(max_digits = 5, decimal_places = 2, db_column = 'Regulatory Score')
#     cluster = models.CharField(max_length = 50, db_column = 'Cluster')
#     highexprsc = models.SmallIntegerField(db_column = 'HighExprSC')
#     highrp = models.SmallIntegerField(db_column = 'HighRP')
#     highexprlm22 = models.SmallIntegerField(db_column = 'HighExprLM22')
#     highexprgse60424 = models.SmallIntegerField(db_column = 'HighExprGSE60424')
#     highexprcomb = models.SmallIntegerField(db_column = 'HighExprComb')

# class tsnePath(models.Model):
#     cancer = models.CharField(max_length = 50, db_column = 'Cancer Type')
#     dataset = models.CharField(max_length = 50, db_column = 'Dataset ID', primary_key = True)
#     original = models.CharField(max_length = 300, db_column = 'Original tsne')
#     annotate = models.CharField(max_length = 300, db_column = 'Annotated tsne')

class UploadGeneFile(models.Model):
    genefile = models.FileField(upload_to = "upload/", db_column = 'Gene File')