from git_code_debt.diff_parser_base import DiffParserBase
from git_code_debt.metric import Metric


class SimpleLineCounterBase(DiffParserBase):
    """Simple counter for various file types and line types."""

    metric_name = None

    def get_metrics_from_stat(self, file_diff_stats):
        metric_value = 0

        for file_diff_stat in file_diff_stats:
            if self.file_check(file_diff_stat.filename):
                for line in file_diff_stat.lines_added:
                    metric_value += 1 if self.line_check(line) else 0
                for line in file_diff_stat.lines_removed:
                    metric_value -= 1 if self.line_check(line) else 0

        yield Metric(self.metric_name, metric_value)

    @property
    def metric_name(self):
        return self.__class__.__name__

    def get_possible_metric_ids(self):
        return [self.metric_name]

    def file_check(self, filename):
        raise NotImplementedError()

    def line_check(self, line):
        raise NotImplementedError()
