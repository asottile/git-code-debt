
import mock
import re

import testify as T

from git_code_debt_server.metric_config import _get_groups_from_yaml
from git_code_debt_server.metric_config import Group


class GroupTest(T.TestCase):
    def test_from_yaml(self):
        # Simulate a call we would get from yaml
        group = Group.from_yaml('BazGroup', **{
            'metrics': ['Foo', 'Bar'],
            'metric_expressions': ['^.*Baz.*$'],
        })

        T.assert_equal(
            group,
            Group('BazGroup', set(['Foo', 'Bar']), (re.compile('^.*Baz.*$'),)),
        )

    def test_contains_does_not_contain(self):
        group = Group('G', set(['Foo', 'Bar']), (re.compile('^.*Baz.*$'),))
        T.assert_is(group.contains('buz'), False)

    def test_contains_contains_by_name(self):
        group = Group('G', set(['Foo', 'Bar']), (re.compile('^.*Baz.*$'),))
        T.assert_is(group.contains('Foo'), True)

    def test_contains_by_regex(self):
        group = Group('G', set(['Foo', 'Bar']), (re.compile('^.*Baz.*$'),))
        T.assert_is(group.contains('FooBaz'), True)


class TestGetGroupsFromYaml(T.TestCase):
    def test_get_groups_from_yaml(self):
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
