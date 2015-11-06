# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('StockFolio', '0005_auto_20151106_1730'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockfoliouser',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, primary_key=True, default=0, auto_created=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stockfoliouser',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
