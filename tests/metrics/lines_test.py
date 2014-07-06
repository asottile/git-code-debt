from __future__ import absolute_import
from __future__ import unicode_literals

from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.metrics.lines import LinesOfCodeParser


def test_lines_of_code_parser():
    parser = LinesOfCodeParser()
    input_stats = [
        FileDiffStat(b'test.py', [b'a'], [], None),
        FileDiffStat(b'womp.yaml', [b'a', b'b', b'c'], [b'hi'], None),
    ]

    metrics = list(parser.get_metrics_from_stat(input_stats))

    expected_value = {
        'TotalLinesOfCode': 3,
        'TotalLinesOfCode_Python': 1,
        'TotalLinesOfCode_Yaml': 2,
    }
    for metric in metrics:
        assert metric.value == expected_value.get(metric.name, 0)
