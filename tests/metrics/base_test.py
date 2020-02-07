from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.file_diff_stat import Status
from git_code_debt.metric import Metric
from git_code_debt.metrics.base import MetricInfo
from git_code_debt.metrics.base import SimpleLineCounterBase
from git_code_debt.metrics.base import TextLineCounterBase
from git_code_debt.repo_parser import BLANK_COMMIT


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

    input_stats = (
        FileDiffStat(
            b'test.py',
            [b'a', b'b', b'c'],
            [b'd'],
            Status.ALREADY_EXISTING,
        ),
    )

    metric, = parser.get_metrics_from_stat(BLANK_COMMIT, input_stats)
    assert metric == Metric('TestCounter', 2)


def test_includes_file_by_default():
    counter = SimpleLineCounterBase()
    file_diff_stat = FileDiffStat(b'filename', [], [], Status.ADDED)
    assert counter.should_include_file(file_diff_stat)


def test_text_line_counter_base():
    class Counter(TextLineCounterBase):
        def text_line_matches_metric(self, line, file_diff_stat):
            return 'foo' in line

    parser = Counter()
    stat = FileDiffStat(b'test.py', [b'hi', b'foo world'], [], Status.ADDED)

    metric, = parser.get_metrics_from_stat(BLANK_COMMIT, (stat,))
    assert metric == Metric('Counter', 1)
