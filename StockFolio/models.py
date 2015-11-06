'''model.py for creating databse and relationship between portfolio and user'''
from django.db import models
from django.contrib.auth.models import User

class StockFolioUser(models.Model):
  '''Add StockFolio data to User'''
  user = models.OneToOneField(User)
  expenditure = models.FloatField(default=0)
  profit = models.FloatField(default=0)

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
    stock_user.expenditure += float(cost_per_share) * int(num_shares)
    if stock_user.profit > 0:
      if stock_user.expenditure > stock_user.profit:
        stock_user.expenditure -= stock_user.profit
        stock_user.profit = 0
      else:
        stock_user.profit -= stock_user.expenditure
        stock_user.expenditure = 0
    stock_user.save()
    result = StockPortfolio.objects.get_or_createt(stock=stock_symbol, user=stock_user)
    result.shares += int(num_shares)
    result.save()

  @staticmethod
  def sell(user_id, stock_symbol, num_shares, cost_per_share):
    '''Create stock row or negate num of shares'''
    stock_user = StockFolioUser.objects.get(user=user_id)
    if float(cost_per_share) * int(num_shares) > expenditure:
      stock_user.profit += (float(cost_per_share) * int(num_shares)) - stock_user.expenditure
    else:
      stock_user.expenditure -= float(cost_per_share) * int(num_shares)
    stock_user.save()
    result = StockPortfolio.objects.get(stock=stock_symbol, user=stock_user)
    if result.shares == 0:
      result.delete()
    else:
      result.shares -= num_shares
      result.save()
