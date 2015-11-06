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
  if request.method == 'POST':
    user_id = request.user.id
    which_form = request.POST.get('which-form', '').strip()
    if which_form == 'find-stock':
      symbol = request.POST.get('stock', '').strip()
      if symbol != '':
        return render(request, 'StockFolio/portfolio.html', {'stock':get_current_info([''+symbol])})
    elif which_form == 'download-historical':
      download_historical(request.POST.get('stock-symbol', '').strip())
    elif which_form == 'buy-stock':
      StockPortfolio.buy(user_id, request.POST.get('stock-symbol', '').strip(), request.POST.get('shares', '').strip(), request.POST.get('cost-per-share', '').strip())
    elif which_form == 'sell-stock':
      StockPortfolio.sell(user_id, request.POST.get('stock-symbol', '').strip(), request.POST.get('shares', '').strip(), request.POST.get('cost-per-share', '').strip())
  return render(request, 'StockFolio/portfolio.html')

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
