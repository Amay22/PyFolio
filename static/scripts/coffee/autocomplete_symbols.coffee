$ ->
  autocomplete_symbols = []
  for key, value of stock_symbols
    autocomplete_symbols.push key + '   '+ value
  $('#input-find-stock').autocomplete
    source: autocomplete_symbols
  return
return