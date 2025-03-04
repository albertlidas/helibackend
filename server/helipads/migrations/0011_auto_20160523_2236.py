# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-23 22:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helipads', '0010_regularuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='latitude_end',
            field=models.FloatField(default=54.65453, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='route',
            name='latitude_start',
            field=models.FloatField(default=43.786543, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='route',
            name='longitude_end',
            field=models.FloatField(default=38.464592, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='route',
            name='longitude_start',
            field=models.FloatField(default=11.5435879, max_length=20),
            preserve_default=False,
        ),
    ]
