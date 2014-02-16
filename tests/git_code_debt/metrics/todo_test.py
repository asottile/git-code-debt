
from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.metric import Metric
from git_code_debt.metrics.todo import TODOCount


def test_parser():
    parser = TODOCount()
    input = [
        FileDiffStat(
            'foo/bar.py',
            ['# TO' + 'DO: herp all the derps', 'womp'],
            [],
            None,
        ),
    ]
    metrics = list(parser.get_metrics_from_stat(input))
    assert metrics == [Metric('TODOCount', 1)]

