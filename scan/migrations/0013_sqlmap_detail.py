# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-05-15 11:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scan', '0012_sqlmap_parameter'),
    ]

    operations = [
        migrations.AddField(
            model_name='sqlmap',
            name='detail',
            field=models.TextField(default=''),
        ),
    ]