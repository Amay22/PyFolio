# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StockFolio', '0002_auto_20151106_0100'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockPortfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('stock', models.CharField(max_length=5)),
                ('shares', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.RenameField(
            model_name='stockfoliouser',
            old_name='money_spent',
            new_name='expenditure',
        ),
        migrations.RemoveField(
            model_name='stockfoliouser',
            name='cash',
        ),
        migrations.RemoveField(
            model_name='stockfoliouser',
            name='portfolio_worth',
        ),
        migrations.AddField(
            model_name='stockportfolio',
            name='user',
            field=models.ForeignKey(to='StockFolio.StockFolioUser'),
        ),
        migrations.AlterUniqueTogether(
            name='stockportfolio',
            unique_together=set([('user', 'stock')]),
        ),
    ]
