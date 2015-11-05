"""views.py to support views for the porfolio of each user"""
from django.shortcuts import render, redirect
# Takes care of checking if the user is logged in or not
from django.contrib.auth.decorators import login_required
# Yahoo YQL stockretiever to get the stock infos
from lib.StockScraper.stockretriever import get_current_info

@login_required
def portfolio(request):
  if request.method == 'POST':
    symbol = request.POST.get('stock', '')
    data = get_current_info(symbol)
    print(data)
  return render(request, 'StockFolio/portfolio.html')
