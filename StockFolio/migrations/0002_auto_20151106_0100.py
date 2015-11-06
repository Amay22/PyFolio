# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StockFolio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockfoliouser',
            name='money_spent',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='stockfoliouser',
            name='portfolio_worth',
            field=models.FloatField(default=0),
        ),
    ]
