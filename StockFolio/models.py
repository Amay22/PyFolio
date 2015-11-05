"""model.py for creating databse and relationship between portfolio and user"""
from django.db import models
from django.contrib.auth.models import User

class StockFolioUser(models.Model):
  """Add StockFolio data to User"""
  user = models.OneToOneField(User)
  cash = models.FloatField(default=100000)
  money_spent = models.FloatField(default=0)
  portfolio_worth = models.FloatField(default=0)
