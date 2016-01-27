;(function(w){
  // 
  // Params
  // 

  var rowH = 23,
      currentYear = (new Date).getFullYear()

  var colors = ["#E29EFF", "#5ee440", "#f25f10", "#f3c401", "#7088ed", "#e06394", "#5be0ad", "#be8058", "#709b32", "#52dbed", "#cb68cf", "#ec605a", "#c4cf8e", "#0398ce", "#a183b1", "#579c74", "#fcb1ef", "#b4d744", "#fe4878", "#eac56d", "#33a254", "#ef4db2", "#6e9592"]

  // 
  // State
  // 
  var allTypes = [],
      selectedTypes = [],
      allCountries = [],
      selectedCountries = [],
      colorBy = 'type',
      showPercent = 100,
      displayCountry = false,
      redraw = function(){},
      redrawTitles = function(){},

      viewport = {
        left: 0,
        top: 0,
        width: 0,
        height: 0,
        containsRect: function(rect) {
          return rectOverlap(rect, {
            x1: this.left,
            x2: this.left + this.width,
            y1: this.top,
            y2: this.top + this.height
          })
        }
      }

  var contentEl = $('#content')

  var updateViewport = function() {
    viewport.left = contentEl.scrollLeft()
    viewport.top = contentEl.scrollTop()
    viewport.width = contentEl.width()
    viewport.height = contentEl.height()
  }

  contentEl.scroll(function () {  
    updateViewport()
    $("#ruler").css({top: viewport.top})
  });

  $(window).resize(updateViewport)

  $(".unckeck-all-types, .check-all-types").click(function(){
    var check = $(this).hasClass('check-all-types')
    $('input[name=selectedTypes]').each(function(){
      this.checked = check
    })
    updateTypes()
  })

  $(".unckeck-all-countries, .check-all-countries").click(function(){
    var check = $(this).hasClass('check-all-countries')
    $('input[name=selectedCountries]').each(function(){
      this.checked = check
    })
    updateCountries()
  })

  $('input[name=color_by]').change(function(){
    colorBy = $('input:checked[name=color_by]').val()
    redraw()
  })

  $('input[name=display_country]').change(function(){
    displayCountry = this.checked
    redrawTitles()
  })

  $('input[name=moreless]').change(function(){
    showPercent = parseInt(this.value, 10)
    redraw()
  })

  w.runHistoryTimeline = function() {
    updateViewport()

    data.people.forEach(function(p, i){
      if (p.to == null || p.to == 0) {
        p.to = currentYear
      }
    })

    // Filter some bugs of lifespan
    data.people = data.people.filter(function(p){
      return p.to - p.from > 0
    })

    // Fill initial selectedTypes
    allTypes = uniqueTop(valuesBy(data.people, 'type'))
    selectedTypes = allTypes

    allCountries = uniqueTop(valuesBy(data.people, 'country'))
    selectedCountries = allCountries

    draw()

    $('body').removeClass('loading')
  }

  //
  // Internal functions
  //

  function draw() {
    // Sort people and assign 'y' positions
    var num = sortPeople(data.people)

    d3.select('.display-people-num').text(num)

    var years = data.people.reduce(function(acc, p) {
      return acc.concat([p.from, p.to])
    }, [])

    var maxY = d3.max(valuesBy(data.people, "index")),
        maxYear = d3.max(years),
        minYear = d3.min(years),
        totalRange = maxYear - minYear,
        w = totalRange * 3, // 3px per year, 30px per decade
        h = maxY * (rowH+1)

    var x = d3.scale.linear()
      .domain([maxYear, minYear])
      .range([0, w])

    var x1 = d3.scale.linear()
      .domain([0, totalRange])
      .range([0, w])

    var y = d3.scale.linear()
      .domain([0, maxY])
      .range([0, h])

    var colorScale = {
      type: d3.scale.ordinal().domain(allTypes).range(colors),
      country: d3.scale.ordinal().domain(allCountries).range(colors)
    }

    var xAxis = d3.svg.axis()
      .scale(x)
      .orient("top")
      .ticks(totalRange / 20)
      .tickFormat(d3.format("1"))

    var ruler = d3.select("#ruler svg")
      .attr("width", w)
      .attr("height", 20)

    ruler.append("g")
      .attr("class", "axis")
      .attr("transform", function(d) { return translate(0, 20) })
      .call(xAxis)


    var typeLabels = d3.select('#type-legend')
      .selectAll('li')
      .data(allTypes)
      .enter().append('li')
        .style("background-color", function(d) { return colorScale.type(d) })
        .append('label')

    typeLabels.append('input')
      .attr('type', 'checkbox')
      .attr('checked', 'checked')
      .attr('name', 'selectedTypes')
      .attr('value', function(d) { return d })
      .on('change', updateTypes)

    typeLabels.append('span')
      .text(function(d) { return d })


    var countryLabels = d3.select('#country-legend')
      .selectAll('li')
      .data(allCountries)
      .enter().append('li')
        .style("background-color", function(d) { return colorScale.country(d) })
        .append('label')

    countryLabels.append('input')
      .attr('type', 'checkbox')
      .attr('checked', 'checked')
      .attr('name', 'selectedCountries')
      .attr('value', function(d) { return d })
      .on('change', updateCountries)

    countryLabels.append('span')
      .text(function(d) { return d })

    var chart = d3.select("#chart")
      .attr("width", w)
      .attr("height", h + rowH)

    var bar = chart.selectAll("g")
      .data(data.people)
      .enter().append("g")
        .attr("transform", function(d) { return translate(x(d.to), y(d.index)) })

    var rect = bar.append("rect")
      .attr("width", function(d) { return x1(d.to - d.from) })
      .attr("height", rowH)
      .attr("fill", function(d) { return colorScale[colorBy](d[colorBy]) })

    var renderTitle = function(d) {
      var styles = [
        'font: 12px Tahoma, Geneva, sans-serif',
        'display: block',
        'margin-left: 10px',
        'line-height: ' + rowH + 'px',
        'max-width: ' + x1(d.to - d.from) + 'px',
        'text-decoration: none',
        'white-space: nowrap',
        'overflow: hidden',
        'text-overflow: ellipsis',
        'color: black'
      ]
      var text = d.name
      if (displayCountry) {
        text += ' (' + d.country + ')'
      }
      return '<a style="' + styles.join(';') + '" href="' + d.link + '" target="_blank">' + text + '</a>'; 
    }

    // Using svg:text is much slower due to lack of native text truncation (ellipsis) support
    // The manual truncation (see wrapText()) works about 30s on 10k people
    // Bisect truncation (see wrapTextBisect()) is 5 times faster than the naive one, but still slow. 
    // That's why we use foreignObject. It is ugly, but much faster.
    var titles = bar.append("foreignObject")
      .attr("width", function(d){ return x1(d.to - d.from) })
      .attr("height", rowH)
      .append("xhtml:body")
        .html(renderTitle)

    redraw = function() {
      // Sort people and assign 'y' positions
      var num = sortPeople(data.people)

      d3.select('.display-people-num').text(num)

      maxY = Math.max(d3.max(valuesBy(data.people, "index")), 0)
      h = maxY * (rowH+1)

      // TODO: investigate why we need to have chart height + rowH
      var chartH = h + rowH

      y.domain([0, maxY]).range([0, h])

      if (chartH > chart.attr("height")) {
        // If height becomes bigger, change immediately
        chart.attr("height", chartH)
      } else {
        // If height becomes lower, change only after animation
        setTimeout(function(){
          chart.attr("height", chartH)
        }, 1000)
      }

      var inViewport = function(d) {
        return viewport.containsRect({
          x1: x(d.to),
          x2: x(d.to) + x1(d.to - d.from),
          y1: y(d.index),
          y2: y(d.index) + rowH,
        }) || viewport.containsRect({
          x1: x(d.to),
          x2: x(d.to) + x1(d.to - d.from),
          y1: y(d.prevIndex),
          y2: y(d.prevIndex) + rowH,
        })
      }
      var notInViewport = function(d) {
        return !inViewport(d)
      }

      bar.filter(function(d){ return d.index == -1 })
        .filter(inViewport)
        .transition()
        .duration(500)
        .style("opacity", 0)
        .each("end", function(){
          this.style.display = "none"
        })

      bar.filter(function(d){ return d.index == -1 })
        .filter(notInViewport)
        .style("opacity", 0)
        .style("display", "none")

      bar.filter(function(d){ return d.index > -1 })
        .style("display", "block")

      bar.filter(function(d){ return d.index > -1 })
        .filter(inViewport)
        .transition()
        .duration(1000)
        .style("opacity", 1)
        .attr("transform", function(d) { return translate(x(d.to), y(d.index)) })

      bar.filter(function(d){ return d.index > -1 })
        .filter(notInViewport)
        .style("opacity", 1)
        .attr("transform", function(d) { return translate(x(d.to), y(d.index)) })

      rect
        .filter(inViewport)
        .transition()
        .duration(1000)
        .attr("fill", function(d){ return colorScale[colorBy](d[colorBy]) })

      rect
        .filter(notInViewport)
        .attr("fill", function(d){ return colorScale[colorBy](d[colorBy]) })
    }

    redrawTitles = function() {
      titles.html(renderTitle)
    }
  }

  function updateTypes() {
    selectedTypes = []
    $('input:checked[name=selectedTypes]').each(function(){
      selectedTypes.push($(this).val())
    })
    redraw()
  }

  function updateCountries() {
    selectedCountries = []
    $('input:checked[name=selectedCountries]').each(function(){
      selectedCountries.push($(this).val())
    })
    redraw()
  }

  function sortPeople(people) {
    people.forEach(function(p){
      p.prevIndex = p.index
    })

    var ys = [], num = 0

    nextPerson:
    for (var i = 0; i < people.length; i++) {
      var p = people[i]

      // Filter out some people
      if (selectedTypes.indexOf(p.type) == -1) {
        p.index = -1
        continue nextPerson
      }
      if (selectedCountries.indexOf(p.country) == -1) {
        p.index = -1
        continue nextPerson
      }
      if (100 / people.length * i > showPercent) {
        p.index = -1
        continue nextPerson
      }

      num++

      nextY:
      for (var j = 0; j < ys.length; j++) {
        // Ensure spans that are already placed on current Y do not intersect
        for (var k = 0; k < ys[j].length; k++) {
          if (Math.min(p.to, ys[j][k].to) - Math.max(p.from, ys[j][k].from) >= 0) {
            continue nextY
          }
        }
        // We can safely place on current Y
        p.index = j
        ys[j].push(p)
        continue nextPerson
      }
      p.index = ys.length
      ys.push([p])
    }

    return num
  }

  function valuesBy(collection, key) {
    return collection.map(function(obj){
      return obj[key]
    })
  }

  function uniqueTop(collection) {
    var values = {}, result = []

    collection.filter(function(val){
      if (typeof val == "undefined") return

      if (typeof values[val] != "undefined") {
        result[values[val]].num++
        return
      }
      values[val] = result.length
      result.push({
        item: val,
        num: 1
      })
    })

    result.sort(function(a,b){
      return b.num - a.num
    })

    return result.map(function(r){
      return r.item
    })
  }

  function translate(x, y) {
    return "translate(" + x + "," + y + ")"
  }

  function rectOverlap(a, b) {
    return a.x1 < b.x2 && a.x2 > b.x1 && a.y1 < b.y2 && a.y2 > b.y1
  }

  function wrapText(width, padding) {
    var self = d3.select(this),
        textLength = self.node().getComputedTextLength(),
        text = self.text();
    while (textLength > (width - 2 * padding) && text.length > 0) {
        text = text.slice(0, -1);
        self.text(text + '...');
        textLength = self.node().getComputedTextLength();
    }
  }

  function wrapTextBisect(width, padding) {
    var self = d3.select(this),
        text = self.text(),
        initLen = text.length
    
    var check = function(textLen, w) {
      self.text(text.substr(0, textLen) + (textLen < initLen ? "..." : ""))
      return self.node().getComputedTextLength() - (w - 2 * padding)
    }

    if (check(initLen, width) < 0) {
      return
    }

    // make an array of lengths though which we will do a search
    var a = Array.apply(null, Array(initLen)).map(function(_, i){ return i })

    d3.bisector(check).left(a, width)
  }
})(window);
