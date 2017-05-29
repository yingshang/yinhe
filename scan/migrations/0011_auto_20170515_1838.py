# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-05-15 10:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scan', '0010_sqlmap_detail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sqlmap',
            old_name='detail',
            new_name='notes',
        ),
        migrations.AddField(
            model_name='sqlmap',
            name='clause',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='sqlmap',
            name='dbms_version',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='sqlmap',
            name='os',
            field=models.TextField(default='', null=True),
        ),
        migrations.AddField(
            model_name='sqlmap',
            name='place',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='sqlmap',
            name='prefix',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='sqlmap',
            name='ptype',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='sqlmap',
            name='post_data',
            field=models.TextField(default='', null=True),
        ),
    ]
