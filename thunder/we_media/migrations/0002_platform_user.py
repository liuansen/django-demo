# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-01-08 02:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('we_media', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='platform',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237'),
            preserve_default=False,
        ),
    ]
