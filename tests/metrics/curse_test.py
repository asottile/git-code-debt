from __future__ import absolute_import
from __future__ import unicode_literals

from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.metric import Metric
from git_code_debt.metrics.curse import CurseWordsParser
from git_code_debt.repo_parser import Commit


def test_curse_words_parser():
    parser = CurseWordsParser()
    input_stats = [
        FileDiffStat(
            b'some/file.rb',
            [b'#man seriously, fuck ruby'],
            [],
            None,
        ),
        FileDiffStat(
            b'cmds/foo.py',
            [b"# I'm clean I swear"],
            [],
            None,
        ),
    ]
    metrics = list(parser.get_metrics_from_stat(Commit.blank, input_stats))
    assert Metric('TotalCurseWords_ruby', 1) in metrics
    assert Metric('TotalCurseWords_python', 0) in metrics
