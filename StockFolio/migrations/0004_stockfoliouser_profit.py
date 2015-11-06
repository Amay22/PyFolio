# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StockFolio', '0003_auto_20151106_0418'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockfoliouser',
            name='profit',
            field=models.FloatField(default=0),
        ),
    ]
