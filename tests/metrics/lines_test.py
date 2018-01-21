from __future__ import absolute_import
from __future__ import unicode_literals

from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.metrics.lines import LinesOfCodeParser
from git_code_debt.repo_parser import Commit


def test_lines_of_code_parser():
    parser = LinesOfCodeParser()
    input_stats = [
        FileDiffStat(b'test.py', [b'a'], [], None),
        FileDiffStat(b'womp.yaml', [b'a', b'b', b'c'], [b'hi'], None),
    ]

    metrics = set(parser.get_metrics_from_stat(Commit.blank, input_stats))

    expected_value = {
        'TotalLinesOfCode': 3,
        'TotalLinesOfCode_python': 1,
        'TotalLinesOfCode_yaml': 2,
    }
    for metric in metrics:
        assert metric.value == expected_value.get(metric.name, 0)
