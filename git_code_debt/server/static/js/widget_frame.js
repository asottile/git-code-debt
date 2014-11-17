$(function () {
    $(window).on('message', function (e) {
        $.ajax({
            url: '/widget/data',
            method: 'POST',
            data: {diff: e.originalEvent.data.diff},
            dataType: 'json',
            success: function (data) {
                parent.postMessage(
                    {
                        metrics: data.metrics,
                        elementId: e.originalEvent.data.elementId
                    },
                    '*'
                );
            }
        });
    });

    parent.postMessage({ready: true}, '*');
});
