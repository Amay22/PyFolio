$ ->
  $('.number').bind 'input propertychange', ->
    $(this).val($(this).val().replace(/\D/g,''))
    return
  return
