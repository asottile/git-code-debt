$(function () {
    $('[data-git-code-debt-domain]').each(function (i, el) {
        var element = $(el),
            debtDomain = element.data('git-code-debt-domain'),
            metricNames = Array.prototype.map.bind(element.find('ul li'))(
                function (li) {
                    return $(li).text();
                }
            ),
            diff = element.find('div').text(),
            iframe = $('<iframe>');

        $(window).on('message', function (e) {
            var originalEvent = e.originalEvent;
            if (originalEvent.data.ready) {
                iframe[0].contentWindow.postMessage(
                    {
                        metricNames: metricNames,
                        diff: diff
                    },
                    '*'
                );
            } else if (originalEvent.data.metrics) {
                iframe.remove();
                element.html($(originalEvent.data.metrics)).show();
            }
        });

        iframe.css({
            border: 0,
            width: 1,
            height: 1,
            position: 'absolute',
            left: -9999
        }).attr('src', debtDomain + '/widget/frame');
        $('body').append(iframe);
    });
});
