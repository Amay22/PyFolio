"""views.py to support views for the porfolio of each user"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from lib.StockScraper.stockretriever import get_current_info

@login_required
def portfolio(request):
  if request.method == 'POST':
    symbol = request.POST.get('stock', '')
    data = get_current_info(symbol)
    print(data)
