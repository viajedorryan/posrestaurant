# Generated by Django 2.0.4 on 2018-05-23 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20180523_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restauranttable',
            name='addedBy',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='restauranttable',
            name='tableStatus',
            field=models.CharField(blank=True, default='Available', max_length=255, null=True),
        ),
    ]
