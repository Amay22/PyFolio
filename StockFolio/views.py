'''views.py to support views for the porfolio of each user'''
from django.shortcuts import render
# Takes care of checking if the user is logged in or not
from django.contrib.auth.decorators import login_required
# Yahoo YQL stockretiever to get the stock infos
from lib.yahoo_stock_scraper.stockretriever import get_current_info, get_historical_info, get_3_month_info, get_news_feed
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
  user_id = request.user.id
  if request.method == 'POST':
    which_form = request.POST.get('which-form', '').strip()
    if which_form == 'find-stock':
      symbol = request.POST.get('stock', '').strip().split(' ')[0].strip().upper()
      if symbol != '':
        portfolio_stock = portfolio_stocks(user_id)
        money = portfolio_stock['money']
        porfolio = portfolio_stock['portfolio_info']
        return render(request, 'StockFolio/portfolio.html', {'stock':get_current_info([''+symbol]), 'news' : get_news_feed(symbol), 'portfolio' : porfolio, 'portfolio_rows' : plot(user_id), 'symbols' : json.dumps(STOCK_SYMBOLS), 'money' : money})
    elif which_form == 'download-historical':
      return download_historical(request.POST.get('stock-symbol', '').strip())
    elif which_form == 'buy-stock':
      symbol = request.POST.get('stock-symbol', '').strip()
      StockPortfolio.buy(user_id, symbol, request.POST.get('shares', '').strip(), request.POST.get('cost-per-share', '').strip())
      portfolio_stock = portfolio_stocks(user_id)
      money = portfolio_stock['money']
      porfolio = portfolio_stock['portfolio_info']
      return render(request, 'StockFolio/portfolio.html', {'stock':get_current_info([''+symbol]), 'news' : get_news_feed(symbol), 'portfolio' : porfolio, 'portfolio_rows' : plot(user_id), 'symbols' : json.dumps(STOCK_SYMBOLS), 'money' : money})
    elif which_form == 'buy-sell':
      symbol = request.POST.get('stock-symbol', '').strip()
      if request.POST.get('buy-stock'):
        StockPortfolio.buy(user_id, symbol, request.POST.get('shares', '').strip(), request.POST.get('cost-per-share', '').strip())
      elif request.POST.get('sell-stock'):
        StockPortfolio.sell(user_id, symbol, request.POST.get('shares', '').strip(), request.POST.get('cost-per-share', '').strip())
      portfolio_stock = portfolio_stocks(user_id)
      money = portfolio_stock['money']
      porfolio = portfolio_stock['portfolio_info']
      return render(request, 'StockFolio/portfolio.html', {'stock':get_current_info([''+symbol]), 'news' : get_news_feed(symbol), 'portfolio' : porfolio, 'portfolio_rows' : plot(user_id), 'symbols' : json.dumps(STOCK_SYMBOLS), 'money' : money})
  portfolio_stock = portfolio_stocks(user_id)
  money = portfolio_stock['money']
  porfolio = portfolio_stock['portfolio_info']
  return render(request, 'StockFolio/portfolio.html', {'portfolio' : porfolio, 'portfolio_rows' : plot(user_id), 'symbols' : json.dumps(STOCK_SYMBOLS), 'money' : money})

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
  user = StockFolioUser.objects.filter(user=user_id)[0]
  money = {'spent' : user.spent, 'earnt' : user.earnt, 'value' : 0, 'profit': '+'}
  if stock_list:
    symbols = [stock.stock for stock in stock_list]
    if len(symbols) == 1:
      stock_data = [get_current_info(symbols)]
    else:
      stock_data = get_current_info(symbols)
    for stock in stock_data:
      for stock_from_list in stock_list:
        if stock_from_list.stock == stock['Symbol']:
          stock['shares'] = stock_from_list.shares
          stock['cost'] = int(stock_from_list.shares) * float(stock['LastTradePriceOnly'])
          money['value'] += float(stock['cost'])
    portfolio_info = [stock_data] if stock_data.__class__ == dict else stock_data
  if float(money['spent']) > (float(money['value']) + float(money['earnt'])):
    money['value'] = '-'
  return {'portfolio_info' : portfolio_info, 'money' : money}

def plot(user_id):
  '''Gets Months of historical info on stock and for the graph plots of portfolio'''
  rows = []
  stocks = StockPortfolio.objects.filter(user=user_id)
  if stocks:
    data = [list(reversed(get_3_month_info(stock.stock))) for stock in stocks]
    days = [day['Date'] for day in data[0]]
    for idx, day in enumerate(days):
      first = True
      for stock_index, stock in enumerate(data):
        if len(stock) <= idx:
          continue
        if first:
          row = {'Value' : round(float(stock[idx]['Close']) * StockPortfolio.objects.filter(stock=stocks[stock_index].stock, user=user_id)[0].shares, 2), 'Date' : day, 'Percent': (float(stock[idx]['Open']) - float(stock[idx]['Close'])) / float(stock[idx]['Close']) * 100, 'Volume': int(stock[idx]['Volume']), 'High': float(stock[idx]['High']), 'Low': float(stock[idx]['Low']), 'AdjClose': float(stock[idx]['AdjClose']), 'Open': float(stock[idx]['Open'])}
          first = False
        else:
          row['Date'] = day
          row['Value'] += round(float(stock[idx]['Close']) * StockPortfolio.objects.filter(stock=stocks[stock_index].stock, user=user_id)[0].shares, 2)
          row['Volume'] += int(stock[idx]['Volume'])
          row['Open'] = (row['Open']  + float(stock[idx]['Open']))/2
          row['High'] = (row['High']  + float(stock[idx]['High']))/2
          row['Low'] = (row['Low']  + float(stock[idx]['Low']))/2
          row['AdjClose'] = (row['AdjClose']  + float(stock[idx]['AdjClose']))/2
          row['Percent'] += (float(stock[idx]['Open']) - float(stock[idx]['Close'])) / float(stock[idx]['Close']) * 100
      rows.append(row)
    rows.reverse()
  return rows
