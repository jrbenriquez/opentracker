# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-16 16:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0007_ticket_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='ticket_link',
            new_name='unique_identifier',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='link',
            new_name='unique_identifier',
        ),
    ]
