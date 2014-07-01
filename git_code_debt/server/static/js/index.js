(function () {
    var STORAGE_KEY = 'hiddenGroups',
        hiddenGroups = JSON.parse(
            window.localStorage.getItem(STORAGE_KEY) || '{}'
        );

    // Hide any initially hidden groups
    (function () {
        var i,
            hidden = Object.keys(hiddenGroups);
        for (var i = 0, length = hidden.length; i < length; i += 1) {
            $('[data-group="' + hidden[i] + '"]').addClass('collapsed');
        }
    } ());

    $('.group-name').click(function () {
        var $this = $(this),
            tbodyParent = $this.parents('tbody');

        tbodyParent.toggleClass('collapsed');

        if (tbodyParent.is('.collapsed')) {
            hiddenGroups[tbodyParent.data('group')] = true;
        } else {
            delete hiddenGroups[tbodyParent.data('group')];
        }

        window.localStorage.setItem(STORAGE_KEY, JSON.stringify(hiddenGroups));
    });
} ());
