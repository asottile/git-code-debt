from __future__ import absolute_import
from __future__ import unicode_literals

from git_code_debt.metrics.base import SimpleLineCounterBase


def is_python_import(line):
    line = line.lstrip()
    if line.startswith(b'import'):
        return True
    if line.startswith(b'from') and b'import' in line:
        return True
    return False


def is_template_import(line):
    line = line.lstrip()
    return (
        line.startswith(b'#') and
        is_python_import(line[1:])
    )


class PythonImportCount(SimpleLineCounterBase):
    def should_include_file(self, file_diff_stat):
        return file_diff_stat.extension == b'.py'

    def line_matches_metric(self, line, file_diff_stat):
        return is_python_import(line)


class CheetahTemplateImportCount(SimpleLineCounterBase):
    def should_include_file(self, file_diff_stat):
        return file_diff_stat.extension == b'.tmpl'

    def line_matches_metric(self, line, file_diff_stat):
        return is_template_import(line)
