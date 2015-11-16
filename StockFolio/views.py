'''views.py to support views for the porfolio of each user'''
from django.shortcuts import render
# Takes care of checking if the user is logged in or not
from django.contrib.auth.decorators import login_required
# Yahoo YQL stockretiever to get the stock infos
from lib.yahoo_stock_scraper.stockretriever import get_current_info, get_historical_info, get_3_month_info
# For workbook to create the historical data of a stock
import xlwt
# Http clients to send the attachment file for historical data
from django.http import HttpResponse
# models i.e. database
from .models import StockPortfolio, StockFolioUser
# Get the global stock ticker symbol
from . import STOCK_SYMBOLS
# Need simplejson to pass dictionart STOCK_SYMBOLS to templates
import json

@login_required
def portfolio(request):
  '''The main method for all the user functionality'''
  print(STOCK_SYMBOLS)
  user_id = request.user.id
  if request.method == 'POST':
    which_form = request.POST.get('which-form', '').strip()
    if which_form == 'find-stock':
      symbol = request.POST.get('stock', '').strip()
      if symbol != '':
        return render(request, 'StockFolio/portfolio.html', {'stock':get_current_info([''+symbol]), 'portfolio' : portfolio_stocks(user_id), 'portfolio_rows' : plot(user_id), 'symbols' : json.dumps(STOCK_SYMBOLS)})
    elif which_form == 'download-historical':
      download_historical(request.POST.get('stock-symbol', '').strip())
    elif which_form == 'buy-stock':
      symbol = request.POST.get('stock-symbol', '').strip()
      StockPortfolio.buy(user_id, symbol, request.POST.get('shares', '').strip(), request.POST.get('cost-per-share', '').strip())
      return render(request, 'StockFolio/portfolio.html', {'stock':get_current_info([''+symbol]), 'portfolio' : portfolio_stocks(user_id), 'portfolio_rows' : plot(user_id), 'symbols' : json.dumps(STOCK_SYMBOLS)})
    elif which_form == 'sell-stock':
      symbol = request.POST.get('stock-symbol', '').strip()
      StockPortfolio.sell(user_id, symbol, request.POST.get('shares', '').strip(), request.POST.get('cost-per-share', '').strip())
      return render(request, 'StockFolio/portfolio.html', {'stock':get_current_info([''+symbol]), 'portfolio' : portfolio_stocks(user_id), 'portfolio_rows' : plot(user_id), 'symbols' : json.dumps(STOCK_SYMBOLS)})
  return render(request, 'StockFolio/portfolio.html', {'portfolio' : portfolio_stocks(user_id), 'portfolio_rows' : plot(user_id), 'symbols' : json.dumps(STOCK_SYMBOLS)})

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
  response['Percentagma'] = 'no-cache'
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
    for stock in stock_data:
      for stock_from_list in stock_list:
        if stock_from_list.stock == stock['Symbol']:
          stock['shares'] = stock_from_list.shares
    portfolio_info = [stock_data] if stock_data.__class__ == dict else stock_data
  return portfolio_info

def plot(user_id):
  '''Gets Months of historical info on stock and for the graph plots of portfolio'''
  rows = []
  stocks = StockPortfolio.objects.filter(user=user_id)
  value = StockFolioUser.objects.filter(user=user_id)[0].expenditure
  if stocks:
    data, closes = [], []
    data = [list(reversed(get_3_month_info(stock.stock))) for stock in stocks]
    days = [day['Date'] for day in data[0]]
    for idx, day in enumerate(days):
      row = {'Value': 0, 'Date': day, 'Percent': 0, 'Volume': 0, 'High': 0, 'Low': 0, 'AdjClose': 0}
      if idx == 0:
        closes = [float(history[idx]['AdjClose']) for history in data]
      else:
        for j, history in enumerate(data):
          ratio = closes[j] / 100
          percent = (float(history[idx]['AdjClose']) - closes[j]) / ratio
          closes[j] = float(history[idx]['AdjClose'])
          if idx > 1:
            value += value * (percent / 100)
          row['Value'] = value
          row['Percent'] += percent
          row['Volume'] += float(history[idx]['Volume'])
          for key in ['High', 'Low', 'AdjClose']:
            row[key] += float(history[idx][key])
        row['Percent'] /= len(data)
        for key in ['High', 'Low', 'AdjClose']:
          row[key] /= len(data)
        rows.append(row)
    rows.reverse()
  return rows
