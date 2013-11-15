import testify as T

from git_code_debt.diff_parser_base import FileDiffStat
from git_code_debt.metrics.base import SimpleLineCounterBase
from git_code_debt.metric import Metric


class TestCounter(SimpleLineCounterBase):

    def file_check(self, filename):
        return True

    def line_check(self, line):
        return True


@T.suite('unit')
class SimpleLineCounterBaseTest(T.TestCase):

    def test_simple_base_counter(self):
        parser = TestCounter()

        T.assert_equal(parser.get_possible_metric_ids(), ['TestCounter'])

        input = [
            FileDiffStat('test.py', ['a', 'b', 'c'], ['d'], 'this_should_be_ignored'),
        ]

        metrics = [item for item in parser.get_metrics_from_stat(input)]
        T.assert_equal(metrics, [Metric('TestCounter', 2)])
