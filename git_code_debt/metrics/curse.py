from __future__ import absolute_import
from __future__ import unicode_literals

import collections

from identify import identify

from git_code_debt.metric import Metric
from git_code_debt.metrics.base import DiffParserBase
from git_code_debt.metrics.base import MetricInfo
from git_code_debt.metrics.common import ALL_TAGS
from git_code_debt.metrics.common import UNKNOWN
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
            filename = file_diff_stat.filename.decode('UTF-8')
            tags = identify.tags_from_filename(filename) or {UNKNOWN}

            for tag in tags:
                curses_by_file_type[tag] += curses_changed

        # Yield overall metric and one per type of expected mapping types
        yield Metric('TotalCurseWords', total_curses)
        for tag, value in curses_by_file_type.items():
            if tag in ALL_TAGS and value:
                yield Metric('TotalCurseWords_{}'.format(tag), value)

    def get_metrics_info(self):
        metric_names = ['TotalCurseWords_{}'.format(tag) for tag in ALL_TAGS]
        metric_names.append('TotalCurseWords')
        return [MetricInfo(metric_name) for metric_name in metric_names]
