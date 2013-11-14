(function(root) {
    var canvas = document.getElementById('graph');
    var context = canvas.getContext('2d');

    var data = [];
    var labels = [];

    for (var i = 0; i < metrics.length; i++) {
        data.push(metrics[i][0]);
        labels.push(metrics[i][1]);
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
        scaleSteps: 10,
        scaleStepWidth: 10,
        scaleStartsValue: 0
    };

    new Chart(context).Line(data, options);
})(this);
