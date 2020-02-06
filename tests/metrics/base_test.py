from __future__ import absolute_import
from __future__ import unicode_literals

from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.metric import Metric
from git_code_debt.metrics.base import DiffParserBase
from git_code_debt.metrics.base import MetricInfo
from git_code_debt.metrics.base import SimpleLineCounterBase
from git_code_debt.metrics.base import TextLineCounterBase
from git_code_debt.repo_parser import Commit


def test_backward_compat_metric_info():
    class MyParser(DiffParserBase):
        def get_possible_metric_ids(self):
            return ['Metric1']

    parser = MyParser()
    info, = parser.get_metrics_info()
    assert info == MetricInfo('Metric1')


def test_simple_base_counter():
    """Smoke test for SimpleLineCounterBase"""
    class TestCounter(SimpleLineCounterBase):
        """This is the test counter!"""

        def should_include_file(self, file_diff_stat):
            return True

        def line_matches_metric(self, line, file_diff_stat):
            return True

    parser = TestCounter()
    info, = parser.get_metrics_info()
    assert info == MetricInfo('TestCounter', 'This is the test counter!')

    input_stats = [
        FileDiffStat(
            'test.py',
            ['a', 'b', 'c'],
            ['d'],
            'this_should_be_ignored',
        ),
    ]

    metric, = parser.get_metrics_from_stat(Commit.blank, input_stats)
    assert metric == Metric('TestCounter', 2)


def test_includes_file_by_default():
    counter = SimpleLineCounterBase()
    assert counter.should_include_file(None)


def test_text_line_counter_base():
    class Counter(TextLineCounterBase):
        def text_line_matches_metric(self, line, file_diff_stat):
            return 'foo' in line

    parser = Counter()
    stats = [FileDiffStat('test.py', [b'hello', b'foo world'], [], 'ignored')]

    metric, = parser.get_metrics_from_stat(Commit.blank, stats)
    assert metric == Metric('Counter', 1)
