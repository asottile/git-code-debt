import testify as T

from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.metrics.lines import LinesOfCodeParser
from testing.base_classes.test import test


@test
def test_lines_of_code_parser():
    parser = LinesOfCodeParser()
    input = [
        FileDiffStat('test.py', ['a'], [], 'this_should_be_ignored'),
        FileDiffStat('womp.yaml', ['a', 'b', 'c'], ['hi'], 'this_should_be_ignored')
    ]

    metrics = list(parser.get_metrics_from_stat(input))

    expected_value = {
        'TotalLinesOfCode': 3,
        'TotalLinesOfCode_Python': 1,
        'TotalLinesOfCode_Yaml': 2,
    }
    for metric in metrics:
        T.assert_equal(metric.value, expected_value.get(metric.name, 0))
