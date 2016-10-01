from __future__ import absolute_import
from __future__ import unicode_literals

import collections

from git_code_debt.metric import Metric
from git_code_debt.metrics.base import DiffParserBase
from git_code_debt.metrics.common import FILE_TYPE_MAP
from git_code_debt.metrics.curse_words import word_list


def count_curse_words(lines):
    curses = 0
    for line in lines:
        for word in line.split():
            if word in word_list:
                curses += 1
    return curses


class CurseWordsParser(DiffParserBase):
    """Counts curse words in a repository, overall and by file type"""

    def get_metrics_from_stat(self, _, file_diff_stats):
        total_curses = 0
        curses_by_file_type = collections.defaultdict(int)

        for file_diff_stat in file_diff_stats:
            curses_added = count_curse_words(file_diff_stat.lines_added)
            curses_removed = count_curse_words(file_diff_stat.lines_removed)
            curses_changed = curses_added - curses_removed

            # Track total overall
            total_curses = total_curses + curses_changed

            # Track by file extension -> type mapping
            file_type = FILE_TYPE_MAP.get(file_diff_stat.extension, 'unknown')
            curses_by_file_type[file_type] += curses_changed

        # Yield overall metric and one per type of expected mapping types
        yield Metric('TotalCurseWords', total_curses)
        for file_type in set(FILE_TYPE_MAP.values()) | set(['unknown']):
            curses_changed = curses_by_file_type.get(file_type, 0)
            yield Metric(
                'TotalCurseWords_{0}'.format(file_type),
                curses_changed,
            )

    def get_possible_metric_ids(self):
        return ['TotalCurseWords'] + [
            'TotalCurseWords_{0}'.format(file_type)
            for file_type in set(FILE_TYPE_MAP.values()) | set(['unknown'])
        ]
