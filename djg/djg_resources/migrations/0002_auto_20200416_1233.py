# Generated by Django 3.0.5 on 2020-04-16 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djg_resources', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='amazonlisting',
            name='id',
        ),
        migrations.RemoveField(
            model_name='amazonparentlisting',
            name='id',
        ),
        migrations.AlterField(
            model_name='amazonlisting',
            name='asin',
            field=models.CharField(max_length=32, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='amazonparentlisting',
            name='parent_asin',
            field=models.CharField(max_length=32, primary_key=True, serialize=False),
        ),
    ]