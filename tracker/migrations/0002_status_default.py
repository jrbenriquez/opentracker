# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-13 13:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='default',
            field=models.BooleanField(default=False),
        ),
    ]
