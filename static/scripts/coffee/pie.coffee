$ ->
  rows = document.getElementById('portfolio-stocks')
  symbol_cost = []
  for row in [0 .. rows.getElementsByClassName('portfolio-stock-symbol').length - 1]
    symbol_cost.push { label : rows.getElementsByClassName('portfolio-stock-symbol')[row].innerText.trim(), value : parseFloat(rows.getElementsByClassName('portfolio-stock-cost')[row].innerText.trim()) }

  pie = new d3pie('pie',
    data: content: symbol_cost
    tooltips:
      enabled: true
      type: 'placeholder'
      string: '{label}: {percentage}%'
      styles:
        fadeInSpeed: 500
        backgroundColor: '#00cc99'
        backgroundOpacity: 0.8
        color: '#ffffcc'
        borderRadius: 4
        font: 'verdana'
        fontSize: 20
        padding: 20)
return