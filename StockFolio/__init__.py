'''Define Global Stock Symbols Constant'''
all_symbols = {}
with open('config/symbols.txt', 'r') as text_file:
  for line in text_file:
    stock = line.split('=')
    all_symbols[stock[0].strip()] = stock[1].strip()

STOCK_SYMBOLS = all_symbols
