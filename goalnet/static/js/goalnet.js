//console.log(goalnetData); 

var width = 960,
    height = 500;

var color = d3.scale.category20();

var force = d3.layout.force()
    .charge(-120)
    .linkDistance(30)
    .size([width, height]);

var svg = d3.select("#network").append("svg")
    .attr("width", width)
    .attr("height", height);

d3.json(goalnetData, function(error, graph) {
  force
      .nodes(graph.nodes)
      .links(graph.links)
      .start();

  var link = svg.selectAll(".link")
      .data(graph.links)
    .enter().append("line")
      .attr("class", "link")
      .style("stroke-width", function(d) { return Math.sqrt(d.value); });

  var node = svg.selectAll(".node")
      .data(graph.nodes)
    .enter().append("circle")
      .attr("class", "node")
      .attr("r", 5)
      .style("fill", function(d) { return color(d.group); })
      .call(force.drag);

  node.append("title")
      .text(function(d) { return d.name; });

  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });
  });
});


// Timeline below the network
var context = cubism.context()
    .step(1e4)
    .size(1100);

// Adds interval markers to timeline
d3.select("#timeline").selectAll(".axis")
    .data(["top", "bottom"])
  .enter().append("div")
    .attr("class", function(d) { return d + " axis"; })
    .each(function(d) { d3.select(this).call(context.axis().ticks(12).orient(d)); });

// Adds line to the hover
// d3.select("#timeline").append("div")
//     .attr("class", "rule")
//     .call(context.rule());

// Adds actual graphs to page
d3.select("#timeline").selectAll(".horizon")
    .data(d3.range(1, 10).map(random))
  .enter().insert("div", ".bottom")
    .attr("class", "horizon")
    .call(context.horizon().extent([-10, 10]));

// Moves chart values w/ mouse over
// context.on("focus", function(i) {
//   d3.selectAll(".value").style("right", i == null ? null : context.size() - i + "px");
// });

// Replace this with context.graphite and graphite.metric!
function random(x) {
  var value = 0,
      values = [],
      i = 0,
      last;
  return context.metric(function(start, stop, step, callback) {
    start = +start, stop = +stop;
    if (isNaN(last)) last = start;
    while (last < stop) {
      last += step;
      value = Math.max(-10, Math.min(10, value + .8 * Math.random() - .4 + .2 * Math.cos(i += x * .02)));
      values.push(value);
    }
    callback(null, values = values.slice((start - stop) / step));
  }, x);
}