from __future__ import annotations

from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.file_diff_stat import Status
from git_code_debt.metric import Metric
from git_code_debt.metrics.todo import TODOCount
from git_code_debt.repo_parser import BLANK_COMMIT


def test_parser():
    parser = TODOCount()
    input_stats = (
        FileDiffStat(
            b'foo/bar.py',
            [b'# TO' + b'DO: herp all the derps', b'womp'],
            [],
            Status.ALREADY_EXISTING,
        ),
    )
    metric, = parser.get_metrics_from_stat(BLANK_COMMIT, input_stats)
    assert metric == Metric('TODOCount', 1)
