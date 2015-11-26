# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StockFolio', '0006_auto_20151106_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockfoliouser',
            name='first_name',
            field=models.CharField(max_length=1, default=''),
        ),
        migrations.AddField(
            model_name='stockfoliouser',
            name='last_name',
            field=models.CharField(max_length=1, default=''),
        ),
    ]
