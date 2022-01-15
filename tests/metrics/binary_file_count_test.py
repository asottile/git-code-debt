from __future__ import annotations

from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.file_diff_stat import SpecialFile
from git_code_debt.file_diff_stat import SpecialFileType
from git_code_debt.file_diff_stat import Status
from git_code_debt.metric import Metric
from git_code_debt.metrics.binary_file_count import BinaryFileCount
from git_code_debt.repo_parser import BLANK_COMMIT


def test_binary_file_count_detects_added():
    parser = BinaryFileCount()
    input_stats = (
        FileDiffStat(
            b'foo', [], [], Status.ADDED,
            special_file=SpecialFile(SpecialFileType.BINARY, b'foo', None),
        ),
    )

    metric, = parser.get_metrics_from_stat(BLANK_COMMIT, input_stats)
    assert metric == Metric('BinaryFileCount', 1)


def test_binary_file_count_detects_deleted():
    parser = BinaryFileCount()
    input_stats = (
        FileDiffStat(
            b'foo', [], [], Status.DELETED,
            special_file=SpecialFile(SpecialFileType.BINARY, None, b'foo'),
        ),
    )

    metric, = parser.get_metrics_from_stat(BLANK_COMMIT, input_stats)
    assert metric == Metric('BinaryFileCount', -1)


def test_binary_file_count_detects_ignores_moved():
    parser = BinaryFileCount()
    input_stats = (
        FileDiffStat(
            b'foo', [], [], Status.ALREADY_EXISTING,
            special_file=SpecialFile(SpecialFileType.BINARY, b'foo', b'foo'),
        ),
    )

    assert not tuple(parser.get_metrics_from_stat(BLANK_COMMIT, input_stats))
