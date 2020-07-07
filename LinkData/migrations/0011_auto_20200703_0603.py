# Generated by Django 3.0.4 on 2020-07-03 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LinkData', '0010_auto_20200625_1302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datacollect',
            name='treatment',
        ),
        migrations.AddField(
            model_name='datacollect',
            name='therapy',
            field=models.CharField(db_column='Therapy', default='None', max_length=50),
        ),
        migrations.AddField(
            model_name='datacollect',
            name='therapy_detailed',
            field=models.CharField(db_column='Detailed Therapy', default='None', max_length=50),
        ),
    ]
