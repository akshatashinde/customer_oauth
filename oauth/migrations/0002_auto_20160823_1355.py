# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-23 13:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baseuser',
            name='is_email_verified',
        ),
        migrations.RemoveField(
            model_name='baseuser',
            name='phone_number',
        ),
    ]
