# Generated by Django 5.0.3 on 2024-07-30 11:13

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
        migrations.AddIndex(
            model_name='question',
            index=django.contrib.postgres.indexes.GinIndex(fields=['search_vector'], name='app_questio_search__e53742_gin'),
        ),
    ]