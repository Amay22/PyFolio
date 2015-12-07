# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StockFolio', '0007_auto_20151126_2350'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockfoliouser',
            old_name='expenditure',
            new_name='earnt',
        ),
        migrations.RenameField(
            model_name='stockfoliouser',
            old_name='profit',
            new_name='spent',
        ),
    ]
