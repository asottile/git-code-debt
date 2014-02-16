$(function() {
    $.plot(
        $('#graph'),
        [window.metrics],
        {
            xaxis: {mode: 'time', timeformat: '%Y-%m-%d'},
            series: {lines: {show: true, fill: true}}
        }
    );

    function setupDatePicker(datePicker, onSelect) {
        datePicker.datepicker({
            onSelect: function() {
                var startDate = $('#datepicker-from').datepicker('getDate');
                var endDate = $('#datepicker-to').datepicker('getDate');

                var startTimestamp = new Date(startDate).getTime() / 1000;
                var endTimestamp = new Date(endDate).getTime() / 1000;

                var url = '?start=' + startTimestamp + '&end=' + endTimestamp;
                window.location = url;
            }
        });

        datePicker.datepicker("setDate", new Date(datePicker.data('timestamp') * 1000));
    }

    setupDatePicker($("#datepicker-from"));
    setupDatePicker($("#datepicker-to"));
});
