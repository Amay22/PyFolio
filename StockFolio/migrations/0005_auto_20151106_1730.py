# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('StockFolio', '0004_stockfoliouser_profit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockfoliouser',
            name='id',
        ),
        migrations.AlterField(
            model_name='stockfoliouser',
            name='user',
            field=models.OneToOneField(serialize=False, primary_key=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
