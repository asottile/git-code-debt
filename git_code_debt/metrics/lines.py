import collections

from git_code_debt.diff_parser_base import DiffParserBase
from git_code_debt.metric import Metric
from git_code_debt.metrics.common import FILE_TYPE_MAP
from git_code_debt_util.path import split_file_path


class LinesOfCodeParser(DiffParserBase):
    """Counts lines of code in a repository, overall and by file types."""

    def get_metrics_from_stat(self, file_diff_stats):
        total_lines = 0
        lines_by_file_type = collections.defaultdict(int)

        for file_diff_stat in file_diff_stats:
            lines_changed = len(file_diff_stat.lines_added) - len(file_diff_stat.lines_removed)

            # Track total overall
            total_lines += lines_changed

            # Track by file extension -> type mapping
            _, _, extension = split_file_path(file_diff_stat.filename)
            file_type = FILE_TYPE_MAP.get(extension, 'unknown')
            lines_by_file_type[file_type] += lines_changed

        # Yield overall metric and one per type of expected mapping types
        yield Metric('TotalLinesOfCode', total_lines)
        for file_type in set(FILE_TYPE_MAP.values()):
            lines_changed = lines_by_file_type.get(file_type, 0)
            yield Metric('TotalLinesOfCode_{0}'.format(file_type), lines_changed)

    def get_possible_metric_ids(self):
        return ['TotalLinesOfCode'] + [
            'TotalLinesOfCode_{0}'.format(file_type)
            for file_type in FILE_TYPE_MAP.values() + ['unknown']
        ]
