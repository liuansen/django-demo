# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-01-10 02:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('we_media', '0002_platform_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='platform',
            name='platform_nickneme',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='\u5e73\u53f0\u8d26\u53f7\u6635\u79f0'),
        ),
    ]
