from __future__ import absolute_import
from __future__ import unicode_literals

import collections
import re

CONFIG_NAMESPACE = 'metric_config'


class Group(collections.namedtuple(
        'Group', ('name', 'metrics', 'metric_expressions'),
)):
    __slots__ = ()

    def contains(self, metric_name):
        return (
            metric_name in self.metrics or
            any(expr.search(metric_name) for expr in self.metric_expressions)
        )

    @classmethod
    def from_yaml(cls, name, metrics, metric_expressions):
        if not metrics and not metric_expressions:
            raise TypeError(
                'Group {} must define at least one of '
                '`metrics` or `metric_expressions`'.format(name),
            )
        return cls(
            name,
            frozenset(metrics),
            tuple(re.compile(expr) for expr in metric_expressions),
        )


def _get_groups_from_yaml(yaml):
    # A group dict maps it's name to a dict containing metrics and
    # metric_expressions
    # Here's an example yaml:
    # [{'Bar': {'metrics': ['Foo', 'Bar'], 'metric_expressions': ['^Baz']}}]
    return tuple(
        Group.from_yaml(
            next(iter(group_dict.keys())),
            next(iter(group_dict.values())).get('metrics', []),
            next(iter(group_dict.values())).get('metric_expressions', []),
        )
        for group_dict in yaml
    )


def _get_commit_links_from_yaml(yaml):
    # The CommitLinks will look like
    # LinkName: 'link_value'
    # OtherLinkName: 'other_link_value'
    # Here we'll alphabetize these and return a tuple of (LinkName, link_value)
    return tuple(sorted(yaml.items()))


class Config(collections.namedtuple(
    'Config', ('color_overrides', 'commit_links', 'groups', 'widget_metrics'),
)):
    __slots__ = ()

    @classmethod
    def from_data(cls, data):
        return cls(
            color_overrides=frozenset(data['ColorOverrides']),
            commit_links=_get_commit_links_from_yaml(data['CommitLinks']),
            groups=_get_groups_from_yaml(data['Groups']),
            widget_metrics=data['WidgetMetrics'],
        )
