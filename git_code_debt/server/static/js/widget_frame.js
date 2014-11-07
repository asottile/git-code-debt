$(function () {
    $(window).on('message', function (e) {
        $.ajax({
            url: '/widget/data',
            method: 'POST',
            data: {
                metric_names: e.originalEvent.data.metricNames,
                diff: e.originalEvent.data.diff
            },
            dataType: 'json',
            success: function (data) {
                parent.postMessage({metrics: data.metrics}, '*');
            }
        });
    });

    parent.postMessage({ready: true}, '*');
});
