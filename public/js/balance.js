
var buildChart = function(points){
   //Draw a graph per user
   var data = [];
   var user_keys = Object.keys(points);
   for (var i=0 ; i< user_keys.length;i++){
     data.push({
       type: "line",
       dataPoints: points[user_keys[i]]
     });
   }
   return new CanvasJS.Chart("graph", {
  		title:{	text: "Weight per month" },
  		data: data
  	});
};

$.ajax({
  url: 'balances',
  success: function(json){
    var points = {};

    for(var i=0; i < json.length; i++){
      w = json[i];

      if (! points[w.user_id]) points[w.user_id] = [];
      points[w.user_id].push({
        x: new Date(w.timestamp*1000),
        y: w.weight
      });
    }
    var chart = buildChart( points);
    chart.render();

  }
});
