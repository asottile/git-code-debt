from __future__ import absolute_import
from __future__ import unicode_literals

import mock
import pytest
import re

import staticconf.errors

from git_code_debt.server.metric_config import _get_groups_from_yaml
from git_code_debt.server.metric_config import Group


def test_Group_from_yaml():
    # Simulate a call we would get from yaml
    group = Group.from_yaml(
        'BazGroup',
        metrics=['Foo', 'Bar'],
        metric_expressions=['^.*Baz.*$'],
    )

    assert (
        group ==
        Group('BazGroup', set(['Foo', 'Bar']), (re.compile('^.*Baz.*$'),))
    )


def test_Group_from_yaml_complains_if_nothing_useful_specified():
    with pytest.raises(staticconf.errors.ValidationError):
        Group.from_yaml('G1', [], [])
        # TODO: assert the exception message
        # 'Group G1 must define at least one of `metrics` or ' +
        # '`metric_expressions`'


def test_Group_contains_does_not_contain():
    group = Group('G', set(['Foo', 'Bar']), (re.compile('^.*Baz.*$'),))
    assert not group.contains('buz')


def test_Group_contains_contains_by_name():
    group = Group('G', set(['Foo', 'Bar']), (re.compile('^.*Baz.*$'),))
    assert group.contains('Foo')


def test_Group_contains_by_regex():
    group = Group('G', set(['Foo', 'Bar']), (re.compile('^.*Baz.*$'),))
    assert group.contains('FooBaz')


def test_get_groups_from_yaml_smoke():
    # Grapped from sample run
    groups_yaml = [
        {'Cheetah': {
            'metrics': [],
            'metric_expressions': ['^.*Cheetah.*$'],
        }},
        {'Python': {
            'metrics': [],
            'metric_expressions': ['^.*Python.*$'],
        }},
        {'CurseWords': {
            'metrics': [],
            'metric_expressions': ['^TotalCurseWords.*$'],
        }},
        {'LinesOfCode': {
            'metrics': [],
            'metric_expressions': ['^TotalLinesOfCode.*$'],
        }}
    ]

    groups = _get_groups_from_yaml(groups_yaml)
    assert (
        groups ==
        (
            # Regexes tested below
            Group('Cheetah', set([]), (mock.ANY,)),
            Group('Python', set([]), (mock.ANY,)),
            Group('CurseWords', set([]), (mock.ANY,)),
            Group('LinesOfCode', set([]), (mock.ANY,)),
        )
    )

    regexes = [group.metric_expressions[0].pattern for group in groups]
    assert (
        regexes ==
        [
            '^.*Cheetah.*$',
            '^.*Python.*$',
            '^TotalCurseWords.*$',
            '^TotalLinesOfCode.*$',
        ]
    )


def test_get_groups_from_yaml_no_metrics_provided():
    groups_yaml = [{'G1': {'metric_expressions': ['^Foo.*$']}}]
    groups = _get_groups_from_yaml(groups_yaml)
    # Regex tested below
    assert groups == (Group('G1', set([]), (mock.ANY,)),)
    assert groups[0].metric_expressions[0].pattern == '^Foo.*$'


def test_get_groups_from_yaml_no_metric_expressions_provided():
    groups_yaml = [{'G1': {'metrics': ['Foo']}}]
    groups = _get_groups_from_yaml(groups_yaml)
    assert groups == (Group('G1', set(['Foo']), tuple()),)
