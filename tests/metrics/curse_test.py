from __future__ import annotations

from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.file_diff_stat import Status
from git_code_debt.metric import Metric
from git_code_debt.metrics.curse import CurseWordsParser
from git_code_debt.repo_parser import BLANK_COMMIT


def test_curse_words_parser():
    parser = CurseWordsParser()
    input_stats = (
        FileDiffStat(
            b'some/file.rb',
            [b'#man seriously, fuck ruby'],
            [],
            Status.ADDED,
        ),
        FileDiffStat(
            b'cmds/foo.py',
            [b"# I'm clean I swear"],
            [],
            Status.ADDED,
        ),
    )
    metrics = set(parser.get_metrics_from_stat(BLANK_COMMIT, input_stats))
    assert metrics == {
        Metric('TotalCurseWords', 1), Metric('TotalCurseWords_ruby', 1),
    }
