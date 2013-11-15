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

    new Chart(context).Line(data, {});

    function setupDatePicker(datePicker, onSelect) {
        datePicker.datepicker({
            onSelect: function() {
                var startDate = $('#datepicker-from').datepicker('getDate');
                var endDate = $('#datepicker-to').datepicker('getDate');

                var startTimestamp = new Date(startDate).getTime() / 1000;
                var endTimestamp = new Date(endDate).getTime() / 1000;

                var url = '?sha=' + sha + '&start=' + startTimestamp + '&end=' + endTimestamp;
                window.location = url;
            }
        });

        datePicker.datepicker("setDate", new Date(datePicker.data('timestamp') * 1000));
    }

    setupDatePicker($("#datepicker-from"));
    setupDatePicker($("#datepicker-to"));
})(this);
