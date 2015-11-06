'''model.py for creating databse and relationship between portfolio and user'''
from django.db import models
from django.contrib.auth.models import User

class StockFolioUser(models.Model):
  '''Add StockFolio data to User'''
  user = models.OneToOneField(User, min_length = 4)
  expenditure = models.FloatField(default=0)

class Stock(models.Model):
  owner = models.ForeignKey(StockFolioUser)
  stock = models.CharField(max_length=5)
  shares = models.PositiveIntegerField(default=0)

  class Meta:
    unique_together = ('owner', 'stock')
