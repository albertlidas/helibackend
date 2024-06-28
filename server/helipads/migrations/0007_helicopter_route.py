# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-13 12:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('helipads', '0006_remove_departure_helicopter'),
    ]

    operations = [
        migrations.AddField(
            model_name='helicopter',
            name='route',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='helipads.Departure'),
            preserve_default=False,
        ),
    ]
