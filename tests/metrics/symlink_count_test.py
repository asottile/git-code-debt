from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.file_diff_stat import SpecialFile
from git_code_debt.file_diff_stat import SpecialFileType
from git_code_debt.file_diff_stat import Status
from git_code_debt.metric import Metric
from git_code_debt.metrics.symlink_count import SymlinkCount
from git_code_debt.repo_parser import BLANK_COMMIT


def test_symlink_count_detects_added():
    parser = SymlinkCount()
    input_stats = (
        FileDiffStat(
            b'foo', [], [], Status.ADDED,
            special_file=SpecialFile(SpecialFileType.SYMLINK, b'bar', None),
        ),
    )

    metric, = parser.get_metrics_from_stat(BLANK_COMMIT, input_stats)
    assert metric == Metric('SymlinkCount', 1)


def test_symlink_count_detects_deleted():
    parser = SymlinkCount()
    input_stats = (
        FileDiffStat(
            b'foo', [], [], Status.DELETED,
            special_file=SpecialFile(SpecialFileType.SYMLINK, None, b'bar'),
        ),
    )

    metric, = parser.get_metrics_from_stat(BLANK_COMMIT, input_stats)
    assert metric == Metric('SymlinkCount', -1)


def test_symlink_count_detects_ignores_moved():
    parser = SymlinkCount()
    input_stats = (
        FileDiffStat(
            b'foo', [], [], Status.ALREADY_EXISTING,
            special_file=SpecialFile(SpecialFileType.SYMLINK, b'bar', b'baz'),
        ),
    )

    assert not tuple(parser.get_metrics_from_stat(BLANK_COMMIT, input_stats))
