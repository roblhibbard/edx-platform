# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-21 18:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0007_scheduleconfig_hold_back_ratio'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='start_date',
            field=models.DateTimeField(blank=True, db_index=True, help_text='Date this schedule went into effect', null=True),
        ),
    ]
