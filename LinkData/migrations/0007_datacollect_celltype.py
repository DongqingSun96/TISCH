# Generated by Django 3.0.4 on 2020-05-20 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LinkData', '0006_uploadgenefile'),
    ]

    operations = [
        migrations.AddField(
            model_name='datacollect',
            name='celltype',
            field=models.CharField(db_column='Cell Type', default='None', max_length=1000),
        ),
    ]