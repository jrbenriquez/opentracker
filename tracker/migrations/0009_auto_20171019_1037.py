# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-19 10:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0008_auto_20171016_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='pause_event',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='task_sub_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='tracker.SubType'),
        ),
    ]