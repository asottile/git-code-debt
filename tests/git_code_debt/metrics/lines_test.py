import testify as T

from git_code_debt.metrics.lines import LinesOfCodeParser
from git_code_debt.diff_parser_base import FileDiffStat


@T.suite('unit')
class LinesOfCodeParserTest(T.TestCase):

    def test_simple_lines(self):
        parser = LinesOfCodeParser()
        input = [
            FileDiffStat('test.py', ['a'], [], 'this_should_be_ignored'),
            FileDiffStat('womp.yaml', ['a', 'b', 'c'], ['hi'], 'this_should_be_ignored')
        ]

        metrics = [item for item in parser.get_metrics_from_stat(input)]

        expected_value = {
            'TotalLinesOfCode': 3,
            'TotalLinesOfCode_Python': 1,
            'TotalLinesOfCode_Yaml': 2,
        }
        for metric in metrics:
            T.assert_equal(metric.value, expected_value.get(metric.metric_name, 0))