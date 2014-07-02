from __future__ import absolute_import
from __future__ import unicode_literals

from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.metric import Metric
from git_code_debt.metrics.base import SimpleLineCounterBase


def test_simple_base_counter():
    """Smoke test for SimpleLineCounterBase"""
    class TestCounter(SimpleLineCounterBase):
        def should_include_file(self, file_diff_stat):
            return True

        def line_matches_metric(self, line, file_diff_stat):
            return True

    parser = TestCounter()
    assert parser.get_possible_metric_ids() == ['TestCounter']

    input_stats = [
        FileDiffStat(
            'test.py',
            ['a', 'b', 'c'],
            ['d'],
            'this_should_be_ignored'
        ),
    ]

    metrics = list(parser.get_metrics_from_stat(input_stats))
    assert metrics == [Metric('TestCounter', 2)]


def test_includes_file_by_default():
    counter = SimpleLineCounterBase()
    assert counter.should_include_file(None)
