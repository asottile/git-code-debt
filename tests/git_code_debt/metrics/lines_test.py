import testify as T

from git_code_debt.metrics.lines import LinesOfCodeParser
from git_code_debt.diff_parser_base import FileDiffStat
from git_code_debt.metric import Metric


@T.suite('unit')
class LinesOfCodeParserTest(T.TestCase):

    def test_simple_lines(self):
        parser = LinesOfCodeParser()
        input = [
            FileDiffStat('test.py', ['a'], [], 'this_should_be_ignored'),
            FileDiffStat('womp.yaml', ['a', 'b', 'c'], ['hi'], 'this_should_be_ignored')
        ]

        metrics = [item for item in parser.get_metrics_from_stat(input)]
        T.assert_equal(metrics, [
            Metric('TotalLinesOfCode', 3),
            Metric('TotalLinesOfCode_Python', 1),
            Metric('TotalLinesOfCode_Yaml', 2),
            Metric('TotalLinesOfCode_Template', 0),
        ])