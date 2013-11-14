(function(root) {
    var canvas = document.getElementById('graph');
    var context = canvas.getContext('2d');

    var data = {
        labels: ['August', 'September', 'October'],
        datasets: [{
            fillColor: "rgba(151, 187, 205, 0.5)",
            strokeColor: "rgba(151, 187, 205, 1)",
            pointColor: "rgba(151, 187, 205, 1)",
            pointStrokeColor: "#fff",
            data: [383, 350, 289]
        }]
    };

    var options = {
        scaleOverride: true,
        scaleSteps: 10,
        scaleStepWidth: 40,
        scaleStartsValue: 0
    };

    new Chart(context).Line(data, options);
})(this);
