from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.metrics.base import SimpleLineCounterBase


class Python__init__LineCount(SimpleLineCounterBase):
    def should_include_file(self, file_diff_stat: FileDiffStat) -> bool:
        return file_diff_stat.filename == b'__init__.py'

    def line_matches_metric(
            self,
            line: bytes,
            file_diff_stat: FileDiffStat,
    ) -> bool:
        # All lines in __init__.py match
        return True
