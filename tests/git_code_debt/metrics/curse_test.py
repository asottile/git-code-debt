import testify as T

from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.metric import Metric
from git_code_debt.metrics.curse import CurseWordsParser
from testing.base_classes.test import test


@test
def test_curse_words_parser():
    parser = CurseWordsParser()
    input = [
        FileDiffStat(
            'templates/foo.tmpl',
            ['#man seriously, fuck cheetah'],
            [],
            None,
        ),
        FileDiffStat(
            'cmds/foo.py',
            ["# I'm clean I swear"],
            [],
            None,
        ),
    ]
    metrics = list(parser.get_metrics_from_stat(input))
    T.assert_in(Metric('TotalCurseWords_Template', 1), metrics)
    T.assert_in(Metric('TotalCurseWords_Python', 0), metrics)

