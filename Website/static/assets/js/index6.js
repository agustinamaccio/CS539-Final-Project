
var formElement = document.getElementById("myForm");
const ctx = document.getElementById('canvas');

formElement.addEventListener("submit", function (event) {
  event.preventDefault(); // prevent page from refreshing
  let iname = document.getElementById('iname').value
let iurl = document.getElementById('iurl').value

  $.ajax({
    url: "/test",
    type: "post",
    data: {'iname': iname, 'iurl' : iurl},
    beforeSend: function(){
      // Show image container
      $("#loader").show();
     },
    success: function(response) {
      $("#loader").hide();
    //   $("#place_for_suggestions").html(response);
      console.log(response)
      $('#a_name').text(response.name)
      $('#a_playlist').text(response.playlist_name)
      $('#a_url').text(response.playlist_link)
//       let mean = response.mean
//       let graph_labels = response.labels
//       // mean.pop()
//       console.log(mean)
//       console.log(graph_labels)
//       console.log(response.new_mean)
//       console.log(response.new_label)
//       let chart1 =  document.getElementById("chart")
//       RadarChart.defaultConfig.color = function() {};
// RadarChart.defaultConfig.radius = 3;
// RadarChart.defaultConfig.w = 400;
// RadarChart.defaultConfig.h = 400;


// let a =[]

var data = [
  {
    className: 'germany', // optional can be used for styling
    axes: [
      {axis: "strength", value: 6}, 
      {axis: "intelligence", value: 8}, 
      {axis: "charisma", value: 11},
      {axis: "dexterity", value: 9},
      {axis: "luck", value: 6}
    ]
  },

];
var chart = RadarChart.chart();
var cfg = chart.config(); // retrieve default config
var svg = d3.select(chart).append('svg')
  .attr('width', cfg.w + cfg.w + 50)
  .attr('height', cfg.h + cfg.h / 4);
svg.append('g').classed('single', 1).datum(data).call(chart);
render();

// graph_labels.map((x, i) => {
//    var result = {'axis':'','value':0};
//    result['axis'] = x
//    result['value'] = mean[i]
//    a.push(result)

//    } );

// graph_labels.map((x, i) => {
//   var result = {'axis':'','value':0};
//   result['axis'] = x
//   result['value'] = mean[i]
//   a.push(result)

//   } );

var data = [
  {
    className: 'graph1', // optional can be used for styling
    axes: a
  },

];



var chart = RadarChart.chart();
var cfg = chart.config(); // retrieve default config
var svg = d3.select(chart1).append('svg')
  .attr('width', cfg.w + cfg.w + 50)
  .attr('height', cfg.h + cfg.h / 4);
svg.append('g').classed('single', 1).datum(data).call(chart);
// RadarChart.draw(chart1,data);
    },
    complete:function(data){
      // Hide image container
      $("#loader").hide();
     },
    error: function(xhr) {
      //Do Something to handle error
    }
  });
});
  
  $(document).ready(function () {
    $(".navbar .nav-link").on("click", function (event) {
      if (this.hash !== "") {
        event.preventDefault();
  
        var hash = this.hash;
  
        $("html, body").animate(
          {
            scrollTop: $(hash).offset().top,
          },
          500,
          function () {
            window.location.hash = hash;
          }
        );
      }
    });
  });
  
  // navbar toggle
  $("#nav-toggle").click(function () {
    $(this).toggleClass("is-active");
    $("ul.nav").toggleClass("show");
  });