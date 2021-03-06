# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-18 02:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collectd_rest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graph',
            name='name',
            field=models.SlugField(max_length=256),
        ),
        migrations.AlterField(
            model_name='graphgroup',
            name='name',
            field=models.SlugField(max_length=256, unique=True),
        ),
    ]
