"""Grabs all the stock Symbols from Nasdaq site"""
__author__ = 'Amay'

import urllib.request

def get_all_symbols():
  '''Gets all the stock ticker symbols and company names'''
  symbols = {}
  try:
    stocks = urllib.request.urlopen('ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt').read().decode('utf-8')
  except:
    return 0
  # remove first line 'Symbol|Security Name|Market Category|Test Issue|Financial Status|Round Lot Size'
  stocks = stocks[stocks.index('\n'):].strip()
  # Remove last line 'File Creation Time: 1116201510:02|||||''
  stocks = stocks[:stocks.rindex('\n')].strip()
  for stock in stocks.split('\n'):
    stock_info = stock.split('|')
    stock_info[1] += '-'
    symbols[stock_info[0]] = stock_info[1][0:stock_info[1].index('-')-1].strip()
  return symbols

def write_symbols_file():
  symbols = get_all_symbols()
  if symbols == 0:
    return
  with open('../../config/symbols.txt', 'w') as text_file:
    for symbol in symbols:
      text_file.write(symbol+'='+symbols[symbol]+'\n')
