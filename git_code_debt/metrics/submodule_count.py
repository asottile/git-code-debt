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


class SubmoduleCount(DiffParserBase):
    """Counts the number of git submodules in a repository."""

    def get_metrics_from_stat(
            self,
            _: Commit,
            file_diff_stats: Tuple[FileDiffStat, ...],
    ) -> Generator[Metric, None, None]:
        submodule_delta = 0

        for file_diff_stat in file_diff_stats:
            if (
                    file_diff_stat.special_file is not None and (
                        file_diff_stat.special_file.file_type is
                        SpecialFileType.SUBMODULE
                    )
            ):
                if file_diff_stat.status is Status.ADDED:
                    submodule_delta += 1
                elif file_diff_stat.status is Status.DELETED:
                    submodule_delta -= 1

        if submodule_delta:
            yield Metric(type(self).__name__, submodule_delta)

    def get_metrics_info(self) -> List[MetricInfo]:
        return [MetricInfo.from_class(type(self))]
