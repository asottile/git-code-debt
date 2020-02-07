from typing import Generator
from typing import List
from typing import Tuple

from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.file_diff_stat import SpecialFileType
from git_code_debt.file_diff_stat import Status
from git_code_debt.metric import Metric
from git_code_debt.metrics.base import DiffParserBase
from git_code_debt.metrics.base import MetricInfo
from git_code_debt.repo_parser import Commit


class SymlinkCount(DiffParserBase):
    """Counts the number of symlinks in the repository."""

    def get_metrics_from_stat(
            self,
            _: Commit,
            file_diff_stats: Tuple[FileDiffStat, ...],
    ) -> Generator[Metric, None, None]:
        symlink_delta = 0

        for file_diff_stat in file_diff_stats:
            if (
                    file_diff_stat.special_file is not None and (
                        file_diff_stat.special_file.file_type is
                        SpecialFileType.SYMLINK
                    )
            ):
                if file_diff_stat.status is Status.ADDED:
                    symlink_delta += 1
                elif file_diff_stat.status is Status.DELETED:
                    symlink_delta -= 1

        if symlink_delta:
            yield Metric(type(self).__name__, symlink_delta)

    def get_metrics_info(self) -> List[MetricInfo]:
        return [MetricInfo.from_class(type(self))]
