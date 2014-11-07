$(function () {
    var idToElements = {},
        thisScript = $('script[src$="/static/js/widget.js"]'),
        debtDomain = thisScript[0].src.split('/static/js/widget.js')[0],
        iframe = $('<iframe>'),
        idToElement = {};

    $(window).on('message', function (e) {
        var targetElement,
            originalEvent = e.originalEvent;

        if (originalEvent.data.ready) {
            $('.git-code-debt').each(function (elementId, el) {
                var element = $(el),
                    metricNames = Array.prototype.map.call(
                        element.find('ul li'),
                        function (li) {
                            return $(li).text();
                        }
                    ),
                    diff = element.find('div').text();

                idToElement[elementId] = element;

                iframe[0].contentWindow.postMessage(
                    {
                        elementId: elementId,
                        metricNames: metricNames,
                        diff: diff
                    },
                    '*'
                );
            });
        } else if (originalEvent.data.metrics) {
            targetElement = idToElement[originalEvent.data.elementId];
            delete idToElement[originalEvent.data.elementId];
            targetElement.html($(originalEvent.data.metrics)).show();

            if ($.isEmptyObject(idToElement)) {
                iframe.remove();
            }
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
