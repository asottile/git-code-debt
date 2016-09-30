from __future__ import absolute_import
from __future__ import unicode_literals

import collections

from git_code_debt.metric import Metric
from git_code_debt.metrics.base import DiffParserBase
from git_code_debt.metrics.common import FILE_TYPE_MAP


class LinesOfCodeParser(DiffParserBase):
    """Counts lines of code in a repository, overall and by file types."""

    def get_metrics_from_stat(self, _, file_diff_stats):
        total_lines = 0
        lines_by_file_type = collections.defaultdict(int)

        for file_diff_stat in file_diff_stats:
            lines_changed = (
                len(file_diff_stat.lines_added) -
                len(file_diff_stat.lines_removed)
            )

            # Track total overall
            total_lines += lines_changed

            # Track by file extension -> type mapping
            file_type = FILE_TYPE_MAP.get(file_diff_stat.extension, 'unknown')
            lines_by_file_type[file_type] += lines_changed

        # Yield overall metric and one per type of expected mapping types
        yield Metric('TotalLinesOfCode', total_lines)
        for file_type in set(FILE_TYPE_MAP.values()) | set(['unknown']):
            lines_changed = lines_by_file_type.get(file_type, 0)
            yield Metric(
                'TotalLinesOfCode_{0}'.format(file_type),
                lines_changed,
            )

    def get_possible_metric_ids(self):
        return ['TotalLinesOfCode'] + [
            'TotalLinesOfCode_{0}'.format(file_type)
            for file_type in set(FILE_TYPE_MAP.values()) | set(['unknown'])
        ]
