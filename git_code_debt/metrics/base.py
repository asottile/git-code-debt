import inspect
from typing import Generator
from typing import List
from typing import NamedTuple
from typing import Tuple
from typing import Type

from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.metric import Metric
from git_code_debt.repo_parser import Commit


class MetricInfo(NamedTuple):
    name: str
    description: str = ''

    @classmethod
    def from_class(cls, c: 'Type[DiffParserBase]') -> 'MetricInfo':
        return cls(c.__name__, inspect.cleandoc(c.__doc__ or ''))


class DiffParserBase:
    # Specify __metric__ = False to not be included (useful for base classes)
    __metric__ = False

    def get_metrics_from_stat(
            self,
            commit: Commit,
            file_diff_stats: Tuple[FileDiffStat, ...],
    ) -> Generator[Metric, None, None]:
        """Implement me to yield Metric objects from the input list of
        FileStat objects.

        Args:
            commit - Commit object
            file_diff_stats - list of FileDiffStat objects

        Returns:
           generator of Metric objects
        """
        raise NotImplementedError

    def get_metrics_info(self) -> List[MetricInfo]:
        raise NotImplementedError


class SimpleLineCounterBase(DiffParserBase):
    __metric__ = False

    def get_metrics_from_stat(
            self,
            _: Commit,
            file_diff_stats: Tuple[FileDiffStat, ...],
    ) -> Generator[Metric, None, None]:
        metric_value = 0

        for file_diff_stat in file_diff_stats:
            if self.should_include_file(file_diff_stat):
                for line in file_diff_stat.lines_added:
                    if self.line_matches_metric(line, file_diff_stat):
                        metric_value += 1
                for line in file_diff_stat.lines_removed:
                    if self.line_matches_metric(line, file_diff_stat):
                        metric_value -= 1

        if metric_value:
            yield Metric(self.metric_name, metric_value)

    def get_metrics_info(self) -> List[MetricInfo]:
        return [MetricInfo(self.metric_name, self.metric_description)]

    @property
    def metric_name(self) -> str:
        """Override me or make a class-level metric_name attribute to set the
        metric name.  Defaults to class name
        """
        return type(self).__name__

    @property
    def metric_description(self) -> str:
        """Override me or make a class-level metric_description attribute to
        set the metric description.  Defaults to metric docstring.
        """
        return inspect.cleandoc(type(self).__doc__ or '')

    def should_include_file(self, file_diff_stat: FileDiffStat) -> bool:
        """Implement me to return whether a filename should be included.
        By default, this returns True.

        :param FileDiffStat file_diff_stat:
        """
        return True

    def line_matches_metric(
            self,
            line: bytes,
            file_diff_stat: FileDiffStat,
    ) -> bool:
        """Implement me to return whether a line matches the metric.

        :param bytes line: Line in the file
        :param FileDiffStat file_diff_stat:
        """
        raise NotImplementedError


class TextLineCounterBase(SimpleLineCounterBase):
    __metric__ = False

    def text_line_matches_metric(
            self,
            line: str,
            file_diff_stat: FileDiffStat,
    ) -> bool:
        raise NotImplementedError

    def line_matches_metric(
            self,
            line: bytes,
            file_diff_stat: FileDiffStat,
    ) -> bool:
        text = line.decode('UTF-8', 'ignore')
        return self.text_line_matches_metric(text, file_diff_stat)
