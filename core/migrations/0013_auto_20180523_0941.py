# Generated by Django 2.0.4 on 2018-05-23 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_salesdenomination'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restauranttable',
            name='updatedBy',
        ),
        migrations.AlterField(
            model_name='restauranttable',
            name='addedBy',
            field=models.CharField(blank=True, default='Available', max_length=255, null=True),
        ),
    ]
