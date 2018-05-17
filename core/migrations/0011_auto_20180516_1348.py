# Generated by Django 2.0.4 on 2018-05-16 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20180515_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurantordersummary',
            name='amountChange',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='restaurantordersummary',
            name='amountTendered',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]