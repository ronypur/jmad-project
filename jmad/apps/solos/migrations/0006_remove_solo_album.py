# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-18 11:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solos', '0005_auto_20170318_0928'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solo',
            name='album',
        ),
    ]
