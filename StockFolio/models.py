'''model.py for creating databse and relationship between portfolio and user'''
from django.db import models
from django.contrib.auth.models import User

class StockFolioUser(models.Model):
  '''Add StockFolio data to User'''
  first_name = models.CharField(default='', max_length=1)
  last_name = models.CharField(default='', max_length=1)
  user = models.OneToOneField(User)
  earnt = models.FloatField(default=0)
  spent = models.FloatField(default=0)

class StockPortfolio(models.Model):
  '''Stock Table to maintain the stock bought'''
  user = models.ForeignKey(StockFolioUser)
  stock = models.CharField(max_length=5)
  shares = models.PositiveIntegerField(default=0)

  class Meta:
    '''The ForeignKey i.e. user and a stock symbol must be unique'''
    unique_together = ('user', 'stock')

  @staticmethod
  def buy(user_id, stock_symbol, num_shares, cost_per_share):
    '''Create stock row or add num of shares'''
    stock_user = StockFolioUser.objects.get(user=user_id)
    stock_user.spent += float(cost_per_share) * int(num_shares)
    stock_user.save()
    result = StockPortfolio.objects.get_or_create(stock=stock_symbol, user=stock_user)[0]
    result.shares += int(num_shares)
    result.save()

  @staticmethod
  def sell(user_id, stock_symbol, num_shares, cost_per_share):
    '''Create stock row or negate num of shares'''
    stock_user = StockFolioUser.objects.get(user=user_id)
    result = StockPortfolio.objects.filter(stock=stock_symbol, user=stock_user)[0]
    result.shares -= int(num_shares)
    if result.shares < 0:
      result.shares = 0
      stock_user.earnt += float(cost_per_share) * result.shares
    else:
      stock_user.earnt += float(cost_per_share) * int(num_shares)
    stock_user.save()
    if result.shares == 0:
      result.delete()
    else:
      result.save()
