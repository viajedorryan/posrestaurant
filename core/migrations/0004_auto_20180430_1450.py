# Generated by Django 2.0.4 on 2018-04-30 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_products'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Products',
            new_name='Product',
        ),
    ]