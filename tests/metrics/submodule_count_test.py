from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.file_diff_stat import SpecialFile
from git_code_debt.file_diff_stat import SpecialFileType
from git_code_debt.file_diff_stat import Status
from git_code_debt.metric import Metric
from git_code_debt.metrics.submodule_count import SubmoduleCount
from git_code_debt.repo_parser import BLANK_COMMIT


def test_submodule_count_detects_added():
    parser = SubmoduleCount()
    input_stats = (
        FileDiffStat(
            b'foo', [], [], Status.ADDED,
            special_file=SpecialFile(SpecialFileType.SUBMODULE, b'bar', None),
        ),
    )

    metric, = parser.get_metrics_from_stat(BLANK_COMMIT, input_stats)
    assert metric == Metric('SubmoduleCount', 1)


def test_submodule_count_detects_deleted():
    parser = SubmoduleCount()
    input_stats = (
        FileDiffStat(
            b'foo', [], [], Status.DELETED,
            special_file=SpecialFile(SpecialFileType.SUBMODULE, None, b'bar'),
        ),
    )

    metric, = parser.get_metrics_from_stat(BLANK_COMMIT, input_stats)
    assert metric == Metric('SubmoduleCount', -1)


def test_submodule_count_detects_ignores_moved():
    parser = SubmoduleCount()
    input_stats = (
        FileDiffStat(
            b'foo', [], [], Status.ALREADY_EXISTING,
            special_file=SpecialFile(SpecialFileType.SUBMODULE, b'br', b'bz'),
        ),
    )

    assert not tuple(parser.get_metrics_from_stat(BLANK_COMMIT, input_stats))
