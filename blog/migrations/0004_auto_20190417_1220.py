# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-04-17 12:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20190417_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_image',
            field=models.ImageField(default='image/user/default.png', upload_to='image/user/%Y/%m', verbose_name='用户头像'),
        ),
    ]
