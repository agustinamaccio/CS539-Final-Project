var formElement = document.getElementById("myForm");
const ctx = document.getElementById("canvas");

formElement.addEventListener("submit", function (event) {
  event.preventDefault(); // prevent page from refreshing
  let iname = document.getElementById("iname").value;
  let iurl = document.getElementById("iurl").value;

  $.ajax({
    url: "/test",
    type: "post",
    data: { iname: iname, iurl: iurl },
    beforeSend: function () {
      // Show image container
      $("#loader").show();
    },
    success: function (response) {
      //   $("#place_for_suggestions").html(response);
      //   console.log(response)
      $("#a_name").text(response.name);
      $("#a_playlist").text(response.playlist_name);
      $("#a_url").text(response.playlist_link);
      let mean = response.mean;
      let graph_labels = response.labels;
      mean.pop();
      let mean2 = response.new_mean;
      let graph_labels2 = response.new_label;
      console.log(response.new_mean);
      console.log(response.new_label);

      let chart1 = document.getElementById("chart");
      let chart2 = document.getElementById("chart2");

      RadarChart.defaultConfig.color = function () {};
      RadarChart.defaultConfig.radius = 3;
      RadarChart.defaultConfig.w = 400;
      RadarChart.defaultConfig.h = 400;

      let a = [];
      let b = [];

      graph_labels.map((x, i) => {
        var result = { axis: "", value: 0 };
        result["axis"] = x;
        result["value"] = mean[i];
        a.push(result);
      });

      graph_labels2.map((x, i) => {
        var result = { axis: "", value: 0 };
        result["axis"] = x;
        result["value"] = mean[i];
        b.push(result);
      });

      var data = [
        {
          className: "graph1", // optional can be used for styling
          axes: a,
        },
      ];
      var data2 = [
        {
          className: "graph1", // optional can be used for styling
          axes: b,
        },
      ];

      var chart = RadarChart.chart();
      var cfg = chart.config(); // retrieve default config
      var svg = d3
        .select(chart1)
        .append("svg")
        .attr("width", cfg.w + cfg.w + 50)
        .attr("height", cfg.h + cfg.h / 4);
      svg.append("g").classed("single", 1).datum(data).call(chart);

      var svg2 = d3
        .select(chart2)
        .append("svg2")
        .attr("width", cfg.w + cfg.w + 50)
        .attr("height", cfg.h + cfg.h / 4);
      svg2.append("g").classed("single", 1).datum(data2).call(chart);

      // RadarChart.draw(chart1,data);
    },
    complete: function (data) {
      // Hide image container
      $("#loader").hide();
    },
    error: function (xhr) {
      //Do Something to handle error
    },
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
