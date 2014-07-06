from __future__ import absolute_import
from __future__ import unicode_literals

from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.metric import Metric
from git_code_debt.metrics.todo import TODOCount


def test_parser():
    parser = TODOCount()
    input_stats = [
        FileDiffStat(
            b'foo/bar.py',
            [b'# TO' + b'DO: herp all the derps', b'womp'],
            [],
            None,
        ),
    ]
    metrics = list(parser.get_metrics_from_stat(input_stats))
    assert metrics == [Metric('TODOCount', 1)]
