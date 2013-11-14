(function(root) {
    var canvas = document.getElementById('graph');
    var context = canvas.getContext('2d');

    var data = [];
    var labels = [];
    var max = 0;
    var steps = 10;

    for (var i = 0; i < metrics.length; i++) {
        data.push(metrics[i][0]);
        labels.push(metrics[i][1]);

        max = Math.max(max, metrics[i][0]);
    }

    var data = {
        labels: labels,
        datasets: [{
            fillColor: "rgba(151, 187, 205, 0.5)",
            strokeColor: "rgba(151, 187, 205, 1)",
            pointColor: "rgba(151, 187, 205, 1)",
            pointStrokeColor: "#fff",
            data: data
        }]
    };

    var options = {
        scaleOverride: true,
        scaleSteps: steps + 1,
        scaleStepWidth: Math.floor(max / steps),
        scaleStartsValue: 0
    };

    new Chart(context).Line(data, options);
})(this);
