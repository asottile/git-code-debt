from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.file_diff_stat import Status
from git_code_debt.metric import Metric
from git_code_debt.metrics.lines_in_init import Python__init__LineCount
from git_code_debt.repo_parser import BLANK_COMMIT


def test_lines_in_init():
    parser = Python__init__LineCount()
    input_stats = (
        FileDiffStat(
            b'testing/__init__.py',
            [b'from .foo import bar'],
            [],
            Status.ADDED,
        ),
    )
    metric, = parser.get_metrics_from_stat(BLANK_COMMIT, input_stats)
    assert metric == Metric('Python__init__LineCount', 1)
