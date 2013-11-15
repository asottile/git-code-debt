import collections

from git_code_debt.diff_parser_base import DiffParserBase
from git_code_debt.metric import Metric
from git_code_debt.metrics.common import FILE_TYPE_MAP
from util.path import split_file_path


def is_python_import(line):
    if line.startswith('import'):
        return True
    if line.startswith('from') and 'import' in line:
        return True
    return False

def is_template_import(line):
    if line.startswith('#import'):
        return True
    return False

# Maps a set of file extensions to a nice name
IMPORT_CHECK_MAP = {
    '.py': is_python_import,
    '.tmpl': is_template_import,
}


class ImportParser(DiffParserBase):
    """Counts number of imports in a repository by file type"""

    def get_metrics_from_stat(self, file_diff_stats):
        imports_by_extension = collections.defaultdict(int)

        for file_diff_stat in file_diff_stats:
            import_count = 0

            _, _, extension = split_file_path(file_diff_stat.filename)
            is_import_line = IMPORT_CHECK_MAP.get(extension, None)
            if is_import_line:
                for line in file_diff_stat.lines_added:
                    import_count += 1 if is_import_line(line) else 0
                for line in file_diff_stat.lines_removed:
                    import_count -= 1 if is_import_line(line) else 0

            imports_by_extension[extension] += import_count

        for extension in IMPORT_CHECK_MAP.keys():
            imports_changed = imports_by_extension.get(extension, 0)
            file_type = FILE_TYPE_MAP.get(extension, 'unknown')
            yield Metric('ImportCount_{0}'.format(file_type), imports_changed)