# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-18 09:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('solos', '0004_auto_20170318_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solo',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albums.Track'),
        ),
    ]
