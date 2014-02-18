
from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.file_diff_stat import Status
from git_code_debt.file_diff_stat import Symlink
from git_code_debt.metric import Metric
from git_code_debt.metrics.symlink_count import SymlinkCount


def test_symlink_count_detects_added():
    parser = SymlinkCount()
    input = [
        FileDiffStat('foo', [], [], Status.ADDED, symlink=Symlink('bar', None)),
    ]

    metrics = list(parser.get_metrics_from_stat(input))
    assert metrics == [Metric('SymlinkCount', 1)]


def test_symlink_count_detects_deleted():
    parser = SymlinkCount()
    input = [
        FileDiffStat('foo', [], [], Status.DELETED, symlink=Symlink(None, 'bar')),
    ]

    metrics = list(parser.get_metrics_from_stat(input))
    assert metrics == [Metric('SymlinkCount', -1)]


def test_symlink_count_detects_ignores_moved():
    parser = SymlinkCount()
    input = [
        FileDiffStat('foo', [], [], Status.ALREADY_EXISTING, symlink=Symlink('bar', 'baz')),
    ]

    metrics = list(parser.get_metrics_from_stat(input))
    assert metrics == [Metric('SymlinkCount', 0)]
