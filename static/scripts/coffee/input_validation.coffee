$ ->
  $('.number').bind 'input propertychange', ->
    $(this).val($(this).val().replace(/\D/g,''))
    return
  $('.sell').bind 'input propertychange', ->
    if parseInt($(this).val()) > parseInt($(this).parent().parent().parent().children('td:nth-child(3)').text())
      $(this).val($(this).val().substring(0, ($(this).val().length-1)))
      alert 'Can only Sell what you own'
    return
  return
