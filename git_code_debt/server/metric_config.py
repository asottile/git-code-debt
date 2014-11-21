from __future__ import absolute_import
from __future__ import unicode_literals

import collections
import re

import staticconf
import staticconf.errors
import staticconf.getters


CONFIG_NAMESPACE = 'metric_config'
metric_config_getter = staticconf.NamespaceGetters(CONFIG_NAMESPACE)


class Group(collections.namedtuple(
        'Group', ['name', 'metrics', 'metric_expressions'],
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
            raise staticconf.errors.ValidationError(
                'Group {0} must define at least one of '
                '`metrics` or `metric_expressions`'.format(name)
            )
        return cls(
            name,
            set(metrics),
            tuple(re.compile(expr) for expr in metric_expressions),
        )


def _get_groups_from_yaml(yaml):
    # A group dict maps it's name to a dict containing metrics and
    # metric_expressions
    # Here's an example yaml:
    # [{'Bar': {'metrics': ['Foo', 'Bar'], 'metric_expressions': ['^Baz']}}]
    return tuple(
        Group.from_yaml(
            list(group_dict.keys())[0],
            list(group_dict.values())[0].get('metrics', []),
            list(group_dict.values())[0].get('metric_expressions', []),
        )
        for group_dict in yaml
    )


def _get_commit_links_from_yaml(yaml):
    # The CommitLinks will look like
    # LinkName: 'link_value'
    # OtherLinkName: 'other_link_value'
    # Here we'll alphabetize these and return a tuple of (LinkName, link_value)
    return tuple(sorted(yaml.items()))


color_overrides = metric_config_getter.get_set('ColorOverrides')

commit_links = staticconf.getters.build_getter(
    _get_commit_links_from_yaml,
    getter_namespace='metric_config',
)('CommitLinks')

groups = staticconf.getters.build_getter(
    _get_groups_from_yaml,
    getter_namespace='metric_config',
)('Groups')

widget_metrics = metric_config_getter.get('WidgetMetrics')
