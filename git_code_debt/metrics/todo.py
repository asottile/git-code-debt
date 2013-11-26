from git_code_debt.metrics.base import SimpleLineCounterBase


class TODOCount(SimpleLineCounterBase):
    def line_matches_metric(self, line, file_diff_stat):
        return 'TODO' in line
