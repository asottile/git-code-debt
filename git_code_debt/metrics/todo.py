from git_code_debt.metrics.base import SimpleLineCounterBase


class TODOCounter(SimpleLineCounterBase):
    metric_name = 'TODOCount'

    def file_check(self, filename):
        return True

    def line_check(self, line):
        return 'TODO' in line
