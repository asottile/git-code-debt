from __future__ import absolute_import

import testify as T

from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.metric import Metric
from git_code_debt.metrics.base import SimpleLineCounterBase

class SimpleLineCounterBaseTest(T.TestCase):

    def test_simple_base_counter(self):
        """Smoke test for SimpleLineCounterBase"""
        class TestCounter(SimpleLineCounterBase):
            def should_include_file(self, file_diff_stat):
                return True
            def line_matches_metric(self, line, file_diff_stat):
                return True

        parser = TestCounter()
        T.assert_equal(parser.get_possible_metric_ids(), ['TestCounter'])

        input = [
            FileDiffStat(
                'test.py',
                ['a', 'b', 'c'],
                ['d'],
                'this_should_be_ignored'
            ),
        ]

        metrics = list(parser.get_metrics_from_stat(input))
        T.assert_equal(metrics, [Metric('TestCounter', 2)])
