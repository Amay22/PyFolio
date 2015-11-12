$ ->
  dim =
    width: 960
    height: 500
    margin:
      top: 20
      right: 50
      bottom: 30
      left: 50
    ohlc: height: 305
    indicator:
      height: 65
      padding: 5
  dim.plot =
    width: dim.width - (dim.margin.left) - (dim.margin.right)
    height: dim.height - (dim.margin.top) - (dim.margin.bottom)
  dim.indicator.top = dim.ohlc.height + dim.indicator.padding
  dim.indicator.bottom = dim.indicator.top + dim.indicator.height + dim.indicator.padding
  indicatorTop = d3.scale.linear().range([
    dim.indicator.top
    dim.indicator.bottom
  ])
  parseDate = d3.time.format('%Y-%m-%d').parse
  zoom = d3.behavior.zoom().on('zoom', draw)
  zoomPercent = d3.behavior.zoom()
  x = techan.scale.financetime().range([
    0
    dim.plot.width
  ])
  y = d3.scale.linear().range([
    dim.ohlc.height
    0
  ])
  yPercent = y.copy()
  # Same as y at this stage, will get a different domain later
  yVolume = d3.scale.linear().range([
    y(0)
    y(0.2)
  ])
  candlestick = techan.plot.candlestick().xScale(x).yScale(y)
  sma0 = techan.plot.sma().xScale(x).yScale(y)
  sma1 = techan.plot.sma().xScale(x).yScale(y)
  ema2 = techan.plot.ema().xScale(x).yScale(y)
  volume = techan.plot.volume().accessor(candlestick.accessor()).xScale(x).yScale(yVolume)
  trendline = techan.plot.trendline().xScale(x).yScale(y)
  supstance = techan.plot.supstance().xScale(x).yScale(y)
  xAxis = d3.svg.axis().scale(x).orient('bottom')
  timeAnnotation = techan.plot.axisannotation().axis(xAxis).format(d3.time.format('%Y-%m-%d')).width(65).translate([
    0
    dim.plot.height
  ])
  yAxis = d3.svg.axis().scale(y).orient('right')
  ohlcAnnotation = techan.plot.axisannotation().axis(yAxis).format(d3.format(',.2fs')).translate([
    x(1)
    0
  ])
  closeAnnotation = techan.plot.axisannotation().axis(yAxis).accessor(candlestick.accessor()).format(d3.format(',.2fs')).translate([
    x(1)
    0
  ])
  percentAxis = d3.svg.axis().scale(yPercent).orient('left').tickFormat(d3.format('+.1%'))
  percentAnnotation = techan.plot.axisannotation().axis(percentAxis)
  volumeAxis = d3.svg.axis().scale(yVolume).orient('right').ticks(3).tickFormat(d3.format(',.3s'))
  volumeAnnotation = techan.plot.axisannotation().axis(volumeAxis).width(35)
  macdScale = d3.scale.linear().range([
    indicatorTop(0) + dim.indicator.height
    indicatorTop(0)
  ])
  rsiScale = macdScale.copy().range([
    indicatorTop(1) + dim.indicator.height
    indicatorTop(1)
  ])
  macd = techan.plot.macd().xScale(x).yScale(macdScale)
  macdAxis = d3.svg.axis().scale(macdScale).ticks(3).orient('right')
  macdAnnotation = techan.plot.axisannotation().axis(macdAxis).format(d3.format(',.2fs')).translate([
    x(1)
    0
  ])
  macdAxisLeft = d3.svg.axis().scale(macdScale).ticks(3).orient('left')
  macdAnnotationLeft = techan.plot.axisannotation().axis(macdAxisLeft).format(d3.format(',.2fs'))
  rsi = techan.plot.rsi().xScale(x).yScale(rsiScale)
  rsiAxis = d3.svg.axis().scale(rsiScale).ticks(3).orient('right')
  rsiAnnotation = techan.plot.axisannotation().axis(rsiAxis).format(d3.format(',.2fs')).translate([
    x(1)
    0
  ])
  rsiAxisLeft = d3.svg.axis().scale(rsiScale).ticks(3).orient('left')
  rsiAnnotationLeft = techan.plot.axisannotation().axis(rsiAxisLeft).format(d3.format(',.2fs'))
  ohlcCrosshair = techan.plot.crosshair().xScale(timeAnnotation.axis().scale()).yScale(ohlcAnnotation.axis().scale()).xAnnotation(timeAnnotation).yAnnotation([
    ohlcAnnotation
    percentAnnotation
    volumeAnnotation
  ]).verticalWireRange([
    0
    dim.plot.height
  ])
  macdCrosshair = techan.plot.crosshair().xScale(timeAnnotation.axis().scale()).yScale(macdAnnotation.axis().scale()).xAnnotation(timeAnnotation).yAnnotation([
    macdAnnotation
    macdAnnotationLeft
  ]).verticalWireRange([
    0
    dim.plot.height
  ])
  rsiCrosshair = techan.plot.crosshair().xScale(timeAnnotation.axis().scale()).yScale(rsiAnnotation.axis().scale()).xAnnotation(timeAnnotation).yAnnotation([
    rsiAnnotation
    rsiAnnotationLeft
  ]).verticalWireRange([
    0
    dim.plot.height
  ])
  svg = d3.select('#portfolio-ohlc').append('svg').attr('width', dim.width).attr('height', dim.height)
  defs = svg.append('defs')
  defs.append('clipPath').attr('id', 'ohlcClip').append('rect').attr('x', 0).attr('y', 0).attr('width', dim.plot.width).attr 'height', dim.ohlc.height
  defs.selectAll('indicatorClip').data([
    0
    1
  ]).enter().append('clipPath').attr('id', (d, i) ->
    'indicatorClip-' + i
  ).append('rect').attr('x', 0).attr('y', (d, i) ->
    indicatorTop i
  ).attr('width', dim.plot.width).attr 'height', dim.indicator.height
  svg = svg.append('g').attr('transform', 'translate(' + dim.margin.left + ',' + dim.margin.top + ')')


  svg.append('g').attr('class', 'x axis').attr 'transform', 'translate(0,' + dim.plot.height + ')'
  ohlcSelection = svg.append('g').attr('class', 'ohlc').attr('transform', 'translate(0,0)')
  ohlcSelection.append('g').attr('class', 'axis').attr('transform', 'translate(' + x(1) + ',0)').append('text').attr('transform', 'rotate(-90)').attr('y', -12).attr('dy', '.71em').style('text-anchor', 'end').text 'Price ($)'
  ohlcSelection.append('g').attr 'class', 'close annotation up'
  ohlcSelection.append('g').attr('class', 'volume').attr 'clip-path', 'url(#ohlcClip)'
  ohlcSelection.append('g').attr('class', 'candlestick').attr 'clip-path', 'url(#ohlcClip)'
  ohlcSelection.append('g').attr('class', 'indicator sma ma-0').attr 'clip-path', 'url(#ohlcClip)'
  ohlcSelection.append('g').attr('class', 'indicator sma ma-1').attr 'clip-path', 'url(#ohlcClip)'
  ohlcSelection.append('g').attr('class', 'indicator ema ma-2').attr 'clip-path', 'url(#ohlcClip)'
  ohlcSelection.append('g').attr 'class', 'percent axis'
  ohlcSelection.append('g').attr 'class', 'volume axis'
  indicatorSelection = svg.selectAll('svg > g.indicator').data([
    'macd'
    'rsi'
  ]).enter().append('g').attr('class', (d) -> d + ' indicator')

  indicatorSelection.append('g').attr('class', 'axis right').attr 'transform', 'translate(' + x(1) + ',0)'
  indicatorSelection.append('g').attr('class', 'axis left').attr 'transform', 'translate(' + x(0) + ',0)'
  indicatorSelection.append('g').attr('class', 'indicator-plot').attr 'clip-path', (d, i) ->
    'url(#indicatorClip-' + i + ')'
  # Add trendlines and other interactions last to be above zoom pane
  svg.append('g').attr 'class', 'crosshair ohlc'
  svg.append('g').attr 'class', 'crosshair macd'
  svg.append('g').attr 'class', 'crosshair rsi'
  svg.append('g').attr('class', 'trendlines analysis').attr 'clip-path', 'url(#ohlcClip)'
  svg.append('g').attr('class', 'supstances analysis').attr 'clip-path', 'url(#ohlcClip)'
  d3.select('#reset-ohlc').on 'click', reset

  reset = ->
    zoom.scale 1
    zoom.translate [
      0
      0
    ]
    draw()
    return

  draw = ->
    zoomPercent.translate zoom.translate()
    zoomPercent.scale zoom.scale()
    svg.select('g.x.axis').call xAxis
    svg.select('g.ohlc .axis').call yAxis
    svg.select('g.volume.axis').call volumeAxis
    svg.select('g.percent.axis').call percentAxis
    svg.select('g.macd .axis.right').call macdAxis
    svg.select('g.rsi .axis.right').call rsiAxis
    svg.select('g.macd .axis.left').call macdAxisLeft
    svg.select('g.rsi .axis.left').call rsiAxisLeft
    # We know the data does not change, a simple refresh that does not perform data joins will suffice.
    svg.select('g.candlestick').call candlestick.refresh
    svg.select('g.close.annotation').call closeAnnotation.refresh
    svg.select('g.volume').call volume.refresh
    svg.select('g .sma.ma-0').call sma0.refresh
    svg.select('g .sma.ma-1').call sma1.refresh
    svg.select('g .ema.ma-2').call ema2.refresh
    svg.select('g.macd .indicator-plot').call macd.refresh
    svg.select('g.rsi .indicator-plot').call rsi.refresh
    svg.select('g.crosshair.ohlc').call ohlcCrosshair.refresh
    svg.select('g.crosshair.macd').call macdCrosshair.refresh
    svg.select('g.crosshair.rsi').call rsiCrosshair.refresh
    svg.select('g.trendlines').call trendline.refresh
    svg.select('g.supstances').call supstance.refresh
    return

  get_parse_data =->
    accessor = candlestick.accessor()

    data_text = 'Date,Open,High,Low,Close,Volume\n'
    rows = document.getElementById('portfolio-time-val-table')
    for row in [1 .. rows.getElementsByClassName('portfolio-table-value').length - 1]
      data_text += rows.getElementsByClassName('portfolio-table-date')[row].innerText.trim() + ','
      data_text += rows.getElementsByClassName('portfolio-table-close')[row-1].innerText.trim() + ','
      data_text += rows.getElementsByClassName('portfolio-table-high')[row].innerText.trim() + ','
      data_text += rows.getElementsByClassName('portfolio-table-low')[row].innerText.trim() + ','
      data_text += rows.getElementsByClassName('portfolio-table-close')[row].innerText.trim() + ','
      data_text += rows.getElementsByClassName('portfolio-table-vol')[row].innerText.trim() + '\n'

    data = d3.csv.parse(data_text.trim()).map((d) ->
      {
        date: parseDate d.Date
        open: +d.Open
        high: +d.High
        low: +d.Low
        close: +d.Close
        volume: +d.Volume
      }
    ).sort((a, b) -> d3.ascending accessor.d(a), accessor.d(b) )

    indicatorPreRoll = 14

    x.domain techan.scale.plot.time(data).domain()
    y.domain techan.scale.plot.ohlc(data.slice(indicatorPreRoll)).domain()
    yPercent.domain techan.scale.plot.percent(y, accessor(data[indicatorPreRoll])).domain()
    yVolume.domain techan.scale.plot.volume(data).domain()
    macdData = techan.indicator.macd()(data)
    macdScale.domain techan.scale.plot.macd(macdData).domain()
    rsiData = techan.indicator.rsi()(data)
    rsiScale.domain techan.scale.plot.rsi(rsiData).domain()
    svg.select('g.candlestick').datum(data).call candlestick
    svg.select('g.close.annotation').datum([ data[data.length - 1] ]).call closeAnnotation
    svg.select('g.volume').datum(data).call volume
    svg.select('g.sma.ma-0').datum(techan.indicator.sma().period(10)(data)).call sma0
    svg.select('g.sma.ma-1').datum(techan.indicator.sma().period(20)(data)).call sma1
    svg.select('g.ema.ma-2').datum(techan.indicator.ema().period(50)(data)).call ema2
    svg.select('g.macd .indicator-plot').datum(macdData).call macd
    svg.select('g.rsi .indicator-plot').datum(rsiData).call rsi
    svg.select('g.crosshair.ohlc').call(ohlcCrosshair).call zoom
    svg.select('g.crosshair.macd').call(macdCrosshair).call zoom
    svg.select('g.crosshair.rsi').call(rsiCrosshair).call zoom
    zoomable = x.zoomable()
    zoomable.domain [
      indicatorPreRoll
      data.length
    ]
    # Zoom in a little to hide indicator preroll
    draw()
    # Associate the zoom with the scale after a domain has been applied
    zoom.x(zoomable).y y
    zoomPercent.y yPercent
    return
  get_parse_data()
return