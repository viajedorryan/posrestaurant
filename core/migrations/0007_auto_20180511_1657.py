# Generated by Django 2.0.4 on 2018-05-11 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_temprestaurantordersummary_isvat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temprestaurantordersummary',
            name='isFloat',
            field=models.BooleanField(default=True),
        ),
    ]
