from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import collections


SIGNS_TO_CLASSNAMES = {
    0: 'metric-none',
    1: 'metric-up',
    -1: 'metric-down',
}


class DeltaPresenter(collections.namedtuple(
        'DeltaPresenter', ['url', 'value'],
)):
    __slots__ = ()

    @property
    def classname(self):
        if not self.value:
            sign = 0
        else:
            sign = self.value // abs(self.value)

        return SIGNS_TO_CLASSNAMES[sign]
