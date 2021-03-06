# Generated by Django 2.0.4 on 2018-05-21 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20180516_1348'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesDenomination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branchCode', models.CharField(blank=True, max_length=255, null=True)),
                ('transactionCode', models.CharField(blank=True, max_length=255, null=True)),
                ('cashier', models.CharField(blank=True, max_length=255, null=True)),
                ('no1k', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('total1k', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('no5h', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('total5h', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('no2h', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('total2h', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('no1h', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('total1h', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('no50p', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('total50p', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('no20p', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('total20p', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('no10p', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('total10p', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('no5p', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('total5p', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('no1p', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('total1p', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('no25c', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('total25c', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
