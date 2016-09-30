from __future__ import absolute_import
from __future__ import unicode_literals

from git_code_debt.file_diff_stat import SpecialFileType
from git_code_debt.file_diff_stat import Status
from git_code_debt.metric import Metric
from git_code_debt.metrics.base import DiffParserBase


class SymlinkCount(DiffParserBase):
    def get_metrics_from_stat(self, _, file_diff_stats):
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

        yield Metric(type(self).__name__, symlink_delta)

    def get_possible_metric_ids(self):
        return [type(self).__name__]
