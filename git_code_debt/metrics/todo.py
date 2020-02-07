from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.metrics.base import SimpleLineCounterBase


class TODOCount(SimpleLineCounterBase):
    def line_matches_metric(
            self,
            line: bytes,
            file_diff_stat: FileDiffStat,
    ) -> bool:
        return b'TODO' in line
