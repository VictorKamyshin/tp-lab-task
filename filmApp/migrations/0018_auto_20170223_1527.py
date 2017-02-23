# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 15:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmApp', '0017_profile_ismoderator'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='activation_key',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='profile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]