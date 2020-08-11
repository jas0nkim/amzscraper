# Generated by Django 3.0.5 on 2020-05-01 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crawl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.TextField()),
                ('domain', models.CharField(max_length=32)),
                ('key_one', models.CharField(blank=True, max_length=32, null=True)),
                ('key_two', models.CharField(blank=True, max_length=32, null=True)),
                ('job_id', models.CharField(db_index=True, max_length=64)),
                ('errors', models.JSONField(blank=True, null=True)),
                ('status', models.SmallIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'rprt_crawls',
            },
        ),
    ]
