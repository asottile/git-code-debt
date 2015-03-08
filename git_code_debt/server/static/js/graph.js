$(function() {
    var graph = $('#graph'),
        changesContainer = $('.changes-container'),
        changesContainerAjaxUrl = changesContainer.data('ajax-url');

    $.plot(
        graph,
        [window.metrics],
        {
            xaxis: {mode: 'time', timeformat: '%Y-%m-%d'},
            series: {lines: {show: true, fill: true}},
            selection: {
                mode: 'x'
            }
        }
    );

    graph.bind('plotselected', function (e, ranges) {
        window.location.href = [
            window.location.pathname,
            '?',
            'start=',
            (ranges.xaxis.from / 1000).toFixed(0).toString(10),
            '&end=',
            (ranges.xaxis.to / 1000).toFixed(0).toString(10)
        ].join('');
    });

    // Ajax load the changes container
    $.getJSON(changesContainerAjaxUrl, function (resp) {
        changesContainer.empty().append($(resp.body));
    });
});
