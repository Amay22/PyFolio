$ ->
  data = []
  rows = document.getElementById('portfolio-time-val-table')
  for row in [0 .. rows.getElementsByClassName('portfolio-table-value').length - 1]
    graph_point = []
    date = rows.getElementsByClassName('portfolio-table-date')[row].innerText.trim().split(/-/gm)
    graph_point.push Date.UTC(parseFloat(date[0]), parseFloat(date[1]) - 1, parseFloat(date[2]))
    graph_point.push parseFloat(rows.getElementsByClassName('portfolio-table-value')[row].innerText.trim().substr(1))
    data.push graph_point
  data.reverse()
  $('#portfolio-time-val-graph').highcharts 'StockChart',
    rangeSelector:
      selected: 2
      inputEnabled: $('#plot').width() > 480
      buttons: [
        {
          type: 'day'
          count: 3
          text: '3d'
        }
        {
          type: 'week'
          count: 1
          text: '1w'
        }
        {
          type: 'week'
          count: 2
          text: '2w'
        }
        {
          type: 'month'
          count: 1
          text: '1m'
        }
        {
          type: 'all'
          text: '3m'
        }
      ]
    title: text: 'Portfolio Value vs Time'
    series: [ {
      name: 'Portfolio Value'
      data: data
      tooltip: valueDecimals: 2
    } ]
    xAxis:
      tickInterval: 24 * 3600 * 1000 * 3
      minRange: 24 * 3600 * 1000 * 3
  return
return