# Generated by Django 3.0.4 on 2020-06-03 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LinkData', '0007_datacollect_celltype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datacollect',
            name='patient',
            field=models.IntegerField(db_column='Patient Number', null=True),
        ),
    ]
