from __future__ import absolute_import
from __future__ import unicode_literals

from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.metric import Metric
from git_code_debt.metrics.lines_in_init import Python__init__LineCount
from git_code_debt.repo_parser import Commit


def test_lines_in_init():
    parser = Python__init__LineCount()
    input_stats = [
        FileDiffStat(
            b'testing/__init__.py',
            [b'from .foo import bar'],
            [],
            None,
        ),
    ]
    metric, = parser.get_metrics_from_stat(Commit.blank, input_stats)
    assert metric == Metric('Python__init__LineCount', 1)
