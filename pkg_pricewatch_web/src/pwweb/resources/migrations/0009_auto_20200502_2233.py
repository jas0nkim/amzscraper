# Generated by Django 3.0.5 on 2020-05-02 22:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0008_auto_20200502_2200'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='amazonlisting',
            table='resrc_amazon_listings',
        ),
        migrations.AlterModelTable(
            name='amazonlistingprice',
            table='resrc_amazon_listing_prices',
        ),
        migrations.AlterModelTable(
            name='amazonparentlisting',
            table='resrc_amazon_parent_listings',
        ),
    ]
