# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-12 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helipads', '0003_helicopter_seats_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='helicopter',
            options={'verbose_name': 'helicopter', 'verbose_name_plural': 'helicopters'},
        ),
        migrations.AddField(
            model_name='helicopter',
            name='image',
            field=models.ImageField(default=3, upload_to=''),
            preserve_default=False,
        ),
    ]
