(function ($) {
    var thisScript = $('script[src$="/static/js/widget.js"]'),
        debtDomain = thisScript[0].src.split('/static/js/widget.js')[0],
        iframe = $('<iframe>'),
        idToElement = {};

    $(window).on('message', function (e) {
        var targetElement, frame,
            originalEvent = e.originalEvent;

        if (originalEvent.data.ready) {
            $('.git-code-debt').each(function (elementId, el) {
                var element = $(el),
                    diff = element.text();

                idToElement[elementId] = element;

                iframe[0].contentWindow.postMessage(
                    {
                        elementId: elementId,
                        diff: diff
                    },
                    '*'
                );
            });
        } else if (originalEvent.data.metrics) {
            targetElement = idToElement[originalEvent.data.elementId];
            delete idToElement[originalEvent.data.elementId];
            frame = $('<iframe scrolling="no" seamless="seamless">');
            frame.css({border: 0, width: 0, height: 0});
            // In firefox, about:blank is loaded asynchronously
            // https://stackoverflow.com/q/10531909/812183
            frame.on('load', function () {
                var reference,
                    frameBody = frame.contents().find('body').css('margin', 0),
                    stylesheet = $('<link>').attr({
                        rel: 'stylesheet',
                        href: debtDomain + '/static/css/git_code_debt.css'
                    });
                frameBody.append(stylesheet);
                reference = $('<div>').css('float', 'left').append(
                    $(originalEvent.data.metrics)
                );
                frameBody.append(reference);
                referenceTable = frameBody.find('table');
                frame[0].contentWindow.setInterval(
                    function () {
                        frame.width(reference.outerWidth(true));
                        frame.height(reference.outerHeight(true));
                    },
                    100
                );
                targetElement.show();
            });
            targetElement.empty().append(frame);

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

    // We loaded another version of jquery so let's attempt to not step
    // on other people's toes.
} (window.jq = $.noConflict(true)));
