# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-12 13:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helipads', '0002_helicopter'),
    ]

    operations = [
        migrations.AddField(
            model_name='helicopter',
            name='seats_number',
            field=models.IntegerField(default=3),
            preserve_default=False,
        ),
    ]
