
from git_code_debt.metrics.base import SimpleLineCounterBase

def is_python_import(line):
    line = line.lstrip()
    if line.startswith('import'):
        return True
    if line.startswith('from') and 'import' in line:
        return True
    return False

def is_template_import(line):
    line = line.lstrip()
    return (
        line.startswith('#') and
        is_python_import(line[1:])
    )

class PythonImportCount(SimpleLineCounterBase):

    def should_include_file(self, file_diff_stat):
        return file_diff_stat.extension == '.py'

    def line_matches_metric(self, line, file_diff_stat):
        return is_python_import(line)

class CheetahTemplateImportCount(SimpleLineCounterBase):

    def should_include_file(self, file_diff_stat):
        return file_diff_stat.extension == '.tmpl'

    def line_matches_metric(self, line, file_diff_stat):
        return is_template_import(line)
