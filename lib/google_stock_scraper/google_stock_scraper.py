"""Use googlefinance to get stock quote"""
__author__ = 'Amay'

import json
from urllib.request import Request, urlopen

GOOG_FINANCE_KEY_TO_FULL_NAME = {
    u'name'   : u'Company',
    u'l'      : u'LastTradePrice',
    u'vo'     : u'Volume',
    u'op'     : u'Open',
    u'hi'     : u'High',
    u'lo'     : u'Low',
    u'mc'     : u'MarketCap',
    u'c'      : u'Change',
    u'cp'     : u'ChangeCap '
}

def build_url(symbol):
  """Creates the Url with the stock symbol that fetches the stock data"""
  return 'http://www.google.com/finance/info?infotype=infoquoteall&q=' + symbol

def request(symbol):
  """Fethes the Json from the url and returns the relevant data"""
  return urlopen(Request(build_url(symbol))).read().decode('ascii', 'ignore').strip()[3:]

def replace_keys(symbol_quotes):
  """Creates the hash for quotes for that stock"""
  quote_key = {}
  for quote in symbol_quotes:
    for key in GOOG_FINANCE_KEY_TO_FULL_NAME:
      if key in quote:
        quote_key[GOOG_FINANCE_KEY_TO_FULL_NAME[key]] = quote[key]
  return quote_key

def quotes(symbols):
  """Return the hash of the end result that is the stock data for the symbol"""
  return replace_keys(json.loads(request(symbols)))
