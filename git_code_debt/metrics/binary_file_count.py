from __future__ import annotations

from typing import Generator

from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.file_diff_stat import SpecialFileType
from git_code_debt.file_diff_stat import Status
from git_code_debt.metric import Metric
from git_code_debt.metrics.base import DiffParserBase
from git_code_debt.metrics.base import MetricInfo
from git_code_debt.repo_parser import Commit


class BinaryFileCount(DiffParserBase):
    """Counts the number of _files_ considered to be binary by `git`."""

    def get_metrics_from_stat(
            self, _: Commit,
            file_diff_stats: tuple[FileDiffStat, ...],
    ) -> Generator[Metric]:
        binary_delta = 0

        for file_diff_stat in file_diff_stats:
            if (
                    file_diff_stat.special_file is not None and (
                        file_diff_stat.special_file.file_type is
                        SpecialFileType.BINARY
                    )
            ):
                if file_diff_stat.status is Status.ADDED:
                    binary_delta += 1
                elif file_diff_stat.status is Status.DELETED:
                    binary_delta -= 1

        if binary_delta:
            yield Metric(type(self).__name__, binary_delta)

    def get_metrics_info(self) -> list[MetricInfo]:
        return [MetricInfo.from_class(type(self))]
