import re
from typing import Any
from typing import Dict
from typing import FrozenSet
from typing import List
from typing import NamedTuple
from typing import Pattern
from typing import Tuple


class Group(NamedTuple):
    name: str
    metrics: FrozenSet[str]
    metric_expressions: Tuple[Pattern[str], ...]

    def contains(self, metric_name: str) -> bool:
        return (
            metric_name in self.metrics or
            any(expr.search(metric_name) for expr in self.metric_expressions)
        )

    @classmethod
    def from_yaml(
            cls,
            name: str,
            metrics: List[str],
            metric_expressions: List[str],
    ) -> 'Group':
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


def _get_groups_from_yaml(yaml: List[Dict[str, Any]]) -> Tuple[Group, ...]:
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


def _get_commit_links_from_yaml(
        yaml: Dict[str, str],
) -> Tuple[Tuple[str, str], ...]:
    # The CommitLinks will look like
    # LinkName: 'link_value'
    # OtherLinkName: 'other_link_value'
    # Here we'll alphabetize these and return a tuple of (LinkName, link_value)
    return tuple(sorted(yaml.items()))


class Config(NamedTuple):
    color_overrides: FrozenSet[str]
    commit_links: Tuple[Tuple[str, str], ...]
    groups: Tuple[Group, ...]
    widget_metrics: List[str]

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> 'Config':
        return cls(
            color_overrides=frozenset(data['ColorOverrides']),
            commit_links=_get_commit_links_from_yaml(data['CommitLinks']),
            groups=_get_groups_from_yaml(data['Groups']),
            widget_metrics=data['WidgetMetrics'],
        )
