from __future__ import absolute_import
from __future__ import unicode_literals

from git_code_debt.metrics.base import SimpleLineCounterBase


class TODOCount(SimpleLineCounterBase):
    def line_matches_metric(self, line, file_diff_stat):
        return b'TODO' in line
