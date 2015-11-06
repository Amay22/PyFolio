'''views.py to support views for the porfolio of each user'''
from django.shortcuts import render
# Takes care of checking if the user is logged in or not
from django.contrib.auth.decorators import login_required
# Yahoo YQL stockretiever to get the stock infos
from lib.yahoo_stock_scraper.stockretriever import get_current_info, get_historical_info
# For workbook to create the historical data of a stock
import xlwt
# Http clients to send the attachment file for historical data
from django.http import HttpResponse
# models i.e. database
from .models import StockPortfolio

@login_required
def portfolio(request):
  '''The main method for all the user functionality'''
  user_id = request.user.id
  if request.method == 'POST':
    which_form = request.POST.get('which-form', '').strip()
    if which_form == 'find-stock':
      symbol = request.POST.get('stock', '').strip()
      if symbol != '':
        return render(request, 'StockFolio/portfolio.html', {'stock':get_current_info([''+symbol]), 'portfolio' : portfolio_stocks(user_id)})
    elif which_form == 'download-historical':
      download_historical(request.POST.get('stock-symbol', '').strip())
    elif which_form == 'buy-stock':
      symbol = request.POST.get('stock-symbol', '').strip()
      StockPortfolio.buy(user_id, symbol, request.POST.get('shares', '').strip(), request.POST.get('cost-per-share', '').strip())
      return render(request, 'StockFolio/portfolio.html', {'stock':get_current_info([''+symbol]), 'portfolio' : portfolio_stocks(user_id)})
    elif which_form == 'sell-stock':
      symbol = request.POST.get('stock-symbol', '').strip()
      StockPortfolio.sell(user_id, symbol, request.POST.get('shares', '').strip(), request.POST.get('cost-per-share', '').strip())
      return render(request, 'StockFolio/portfolio.html', {'stock':get_current_info([''+symbol]), 'portfolio' : portfolio_stocks(user_id)})
  return render(request, 'StockFolio/portfolio.html', {'portfolio' : portfolio_stocks(user_id)})

def download_historical(symbol):
  '''Downloads the historical data to the desktop'''
  stock_history = get_historical_info(symbol)
  book = xlwt.Workbook()
  sheet = book.add_sheet('Sheet')
  for idx, key in enumerate(stock_history[0].keys()):
    sheet.write(0, idx, key)
  for idx, row in enumerate(stock_history, start=1):
    for col, val in enumerate(row.values()):
      sheet.write(idx, col, val)
  response = HttpResponse(content_type='application/x-msexcel')
  response['Pragma'] = 'no-cache'
  response['Content-disposition'] = 'attachment; filename=' + symbol + '-history.xls'
  book.save(response)
  return response

def portfolio_stocks(user_id):
  '''Returns the list of stocks in a users portfolio'''
  portfolio_info = []
  stock_list = StockPortfolio.objects.filter(user=user_id)
  if stock_list:
    symbols = [stock.stock for stock in stock_list]
    stock_data = get_current_info(symbols)
    for stock in [stock_data]:
      for stock_from_list in stock_list:
        if stock_from_list.stock == stock['Symbol']:
          stock['shares'] = stock_from_list.shares
    portfolio_info = [stock_data] if stock_data.__class__ == dict else stock_data
  return portfolio_info

