# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-07-25 19:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gas_app', '0002_auto_20190725_0118'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='car_name',
            new_name='name',
        ),
        migrations.AddField(
            model_name='car',
            name='make',
            field=models.CharField(default='toyota', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='car',
            name='model',
            field=models.CharField(default='avalon', max_length=255),
            preserve_default=False,
        ),
    ]
