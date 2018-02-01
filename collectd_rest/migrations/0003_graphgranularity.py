# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-18 03:29
from __future__ import unicode_literals

import collectd_rest.models
from django.db import migrations, models
import django.db.models.deletion

def forward_default_graph_granularity(apps, schema_editor):
    GraphGranularity = apps.get_model("collectd_rest", "GraphGranularity")
    db_alias = schema_editor.connection.alias
    objects = GraphGranularity.objects.using(db_alias)
    objects.create(name='default', max_age=0)

def reverse_default_graph_granularity(apps, schema_editor):
    GraphGranularity = apps.get_model("collectd_rest", "GraphGranularity")
    db_alias = schema_editor.connection.alias
    objects = GraphGranularity.objects.using(db_alias)
    objects.get(name='default').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('collectd_rest', '0002_slug_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='GraphGranularity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(max_length=256, unique=True)),
                ('max_age', models.PositiveIntegerField()),
            ],
        ),
        # collectd_rest.models.default_graph_granularity implies that object
        # with name='default' exists
        migrations.RunPython(
            forward_default_graph_granularity,
            reverse_default_graph_granularity
        ),
        migrations.AddField(
            model_name='graph',
            name='granularity',
            field=models.ForeignKey(default=collectd_rest.models.default_graph_granularity, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='graphs', to='collectd_rest.GraphGranularity'),
        ),
    ]