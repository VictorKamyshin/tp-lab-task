# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-21 22:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmApp', '0015_auto_20170219_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='time of comment'),
        ),
    ]
