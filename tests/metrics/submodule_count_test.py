from __future__ import absolute_import
from __future__ import unicode_literals

from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.file_diff_stat import SpecialFile
from git_code_debt.file_diff_stat import SpecialFileType
from git_code_debt.file_diff_stat import Status
from git_code_debt.metric import Metric
from git_code_debt.metrics.submodule_count import SubmoduleCount


def test_submodule_count_detects_added():
    parser = SubmoduleCount()
    input_stats = [
        FileDiffStat(
            'foo', [], [], Status.ADDED,
            special_file=SpecialFile(SpecialFileType.SUBMODULE, 'bar', None),
        ),
    ]

    metrics = list(parser.get_metrics_from_stat(input_stats))
    assert metrics == [Metric('SubmoduleCount', 1)]


def test_submodule_count_detects_deleted():
    parser = SubmoduleCount()
    input_stats = [
        FileDiffStat(
            'foo', [], [], Status.DELETED,
            special_file=SpecialFile(SpecialFileType.SUBMODULE, None, 'bar'),
        ),
    ]

    metrics = list(parser.get_metrics_from_stat(input_stats))
    assert metrics == [Metric('SubmoduleCount', -1)]


def test_submodule_count_detects_ignores_moved():
    parser = SubmoduleCount()
    input_stats = [
        FileDiffStat(
            'foo', [], [], Status.ALREADY_EXISTING,
            special_file=SpecialFile(SpecialFileType.SUBMODULE, 'bar', 'baz'),
        ),
    ]

    metrics = list(parser.get_metrics_from_stat(input_stats))
    assert metrics == [Metric('SubmoduleCount', 0)]
