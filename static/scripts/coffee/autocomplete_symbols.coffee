$ ->
  autocomplete_symbols = []
  for key, value of stock_symbols
    autocomplete_symbols.push key + '   '+ value
  $('#input-find-stock').autocomplete
    source: autocomplete_symbols
  $('form#find-stock').submit ->
    if $('#input-find-stock').val() not in autocomplete_symbols
      $('#input-find-stock').val('')
      alert 'This Stock doesn\'t exist'
    return
  return
