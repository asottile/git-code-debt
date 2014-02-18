
from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.file_diff_stat import Status
from git_code_debt.file_diff_stat import Submodule
from git_code_debt.metric import Metric
from git_code_debt.metrics.submodule_count import SubmoduleCount


def test_submodule_count_detects_added():
    parser = SubmoduleCount()
    input = [
        FileDiffStat('foo', [], [], Status.ADDED, submodule=Submodule('bar', None)),
    ]

    metrics = list(parser.get_metrics_from_stat(input))
    assert metrics == [Metric('SubmoduleCount', 1)]


def test_submodule_count_detects_deleted():
    parser = SubmoduleCount()
    input = [
        FileDiffStat('foo', [], [], Status.DELETED, submodule=Submodule(None, 'bar')),
    ]

    metrics = list(parser.get_metrics_from_stat(input))
    assert metrics == [Metric('SubmoduleCount', -1)]


def test_submodule_count_detects_ignores_moved():
    parser = SubmoduleCount()
    input = [
        FileDiffStat('foo', [], [], Status.ALREADY_EXISTING, submodule=Submodule('bar', 'baz')),
    ]

    metrics = list(parser.get_metrics_from_stat(input))
    assert metrics == [Metric('SubmoduleCount', 0)]
