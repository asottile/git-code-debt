from __future__ import absolute_import
from __future__ import unicode_literals

from git_code_debt.metric import Metric


class DiffParserBase(object):
    """Generates metrics from git show"""
    # Specify __metric__ = False to not be included (useful for base classes)
    __metric__ = False

    def get_metrics_from_stat(self, commit, file_diff_stats):
        """Implement me to yield Metric objects from the input list of
        FileStat objects.

        Args:
            commit - Commit object
            file_diff_stats - list of FileDiffStat objects

        Returns:
           generator of Metric objects
        """
        raise NotImplementedError

    def get_possible_metric_ids(self):
        raise NotImplementedError


class SimpleLineCounterBase(DiffParserBase):
    """Simple counter for various file types and line types."""
    __metric__ = False

    def get_metrics_from_stat(self, _, file_diff_stats):
        metric_value = 0

        for file_diff_stat in file_diff_stats:
            if self.should_include_file(file_diff_stat):
                for line in file_diff_stat.lines_added:
                    if self.line_matches_metric(line, file_diff_stat):
                        metric_value += 1
                for line in file_diff_stat.lines_removed:
                    if self.line_matches_metric(line, file_diff_stat):
                        metric_value -= 1

        yield Metric(self.metric_name, metric_value)

    def get_possible_metric_ids(self):
        return [self.metric_name]

    @property
    def metric_name(self):
        """Override me or make a class-level metric_name attribute to set the
        metric name.
        """
        return type(self).__name__

    def should_include_file(self, file_diff_stat):
        """Implement me to return whether a filename should be included.
        By default, this returns True.

        :param FileDiffStat file_diff_stat:
        """
        return True

    def line_matches_metric(self, line, file_diff_stat):
        """Implement me to return whether a line matches the metric.

        :param bytes line: Line in the file
        :param FileDiffStat file_diff_stat:
        """
        raise NotImplementedError
