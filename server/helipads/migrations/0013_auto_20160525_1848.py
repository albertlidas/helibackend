# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-25 18:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helipads', '0012_auto_20160524_1837'),
    ]

    operations = [
        migrations.RenameField(
            model_name='helicopter',
            old_name='seats_number',
            new_name='seats_count',
        ),
    ]
