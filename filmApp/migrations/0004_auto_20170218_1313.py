# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 13:13
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('filmApp', '0003_auto_20170218_1242'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='appraisal',
            managers=[
                ('myManager', django.db.models.manager.Manager()),
            ],
        ),
    ]
