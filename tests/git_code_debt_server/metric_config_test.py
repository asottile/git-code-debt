
import mock
import re

import staticconf.errors
import testify as T

from git_code_debt_server.metric_config import _get_groups_from_yaml
from git_code_debt_server.metric_config import Group
from testing.base_classes.test import test


@test
def test_Group_from_yaml():
    # Simulate a call we would get from yaml
    group = Group.from_yaml('BazGroup', **{
        'metrics': ['Foo', 'Bar'],
        'metric_expressions': ['^.*Baz.*$'],
    })

    T.assert_equal(
        group,
        Group('BazGroup', set(['Foo', 'Bar']), (re.compile('^.*Baz.*$'),)),
    )

@test
def test_Group_from_yaml_complains_if_nothing_useful_specified():
    with T.assert_raises_exactly(
        staticconf.errors.ValidationError,
        'Group G1 must define at least one of `metrics` or `metric_expressions`'
    ):
        Group.from_yaml('G1', [], [])

@test
def test_Group_contains_does_not_contain():
    group = Group('G', set(['Foo', 'Bar']), (re.compile('^.*Baz.*$'),))
    T.assert_is(group.contains('buz'), False)

@test
def test_Group_contains_contains_by_name():
    group = Group('G', set(['Foo', 'Bar']), (re.compile('^.*Baz.*$'),))
    T.assert_is(group.contains('Foo'), True)

@test
def test_Group_contains_by_regex():
    group = Group('G', set(['Foo', 'Bar']), (re.compile('^.*Baz.*$'),))
    T.assert_is(group.contains('FooBaz'), True)


@test
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
    T.assert_equal(
        groups,
        (
            # Regexes tested below
            Group('Cheetah', set([]), (mock.ANY,)),
            Group('Python', set([]), (mock.ANY,)),
            Group('CurseWords', set([]), (mock.ANY,)),
            Group('LinesOfCode', set([]), (mock.ANY,)),
        ),
    )

    regexes = [group.metric_expressions[0].pattern for group in groups]
    T.assert_equal(
        regexes,
        [
            '^.*Cheetah.*$',
            '^.*Python.*$',
            '^TotalCurseWords.*$',
            '^TotalLinesOfCode.*$',
        ],
    )

@test
def test_get_groups_from_yaml_no_metrics_provided():
    groups_yaml = [{'G1': {'metric_expressions': ['^Foo.*$']}}]
    groups = _get_groups_from_yaml(groups_yaml)
    # Regex tested below
    T.assert_equal(groups, (Group('G1', set([]), (mock.ANY,)),))
    T.assert_equal(groups[0].metric_expressions[0].pattern, '^Foo.*$')

@test
def test_get_groups_from_yaml_no_metric_expressions_provided():
    groups_yaml = [{'G1': {'metrics': ['Foo']}}]
    groups = _get_groups_from_yaml(groups_yaml)
    T.assert_equal(groups, (Group('G1', set(['Foo']), tuple()),))
