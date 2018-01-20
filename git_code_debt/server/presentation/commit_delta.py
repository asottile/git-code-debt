from __future__ import absolute_import
from __future__ import unicode_literals

import collections


class CommitDelta(collections.namedtuple(
        'CommitDelta', ('metric_name', 'classname', 'delta'),
)):
    __slots__ = ()

    @classmethod
    def from_data(cls, metric_name, delta, color_overrides):
        return cls(
            metric_name,
            # TODO: duplicated in Metric
            'color-override' if metric_name in color_overrides else '',
            delta,
        )
