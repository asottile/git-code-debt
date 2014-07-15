from __future__ import absolute_import
from __future__ import unicode_literals

import collections

from git_code_debt.server import metric_config


class CommitDeltaPresenter(collections.namedtuple(
        'CommitDeltaPresenter', ['metric_name', 'classname', 'delta'],
)):
    __slots__ = ()

    @classmethod
    def from_data(cls, metric_name, delta_presenter):
        return cls(
            metric_name,
            # TODO: duplicated in MetricPresenter
            (
                'color-override'
                if metric_name in metric_config.color_overrides
                else ''
            ),
            delta_presenter,
        )
