import testify as T

from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.metric import Metric
from git_code_debt.metrics.imports import CheetahTemplateImportCount
from git_code_debt.metrics.imports import is_python_import
from git_code_debt.metrics.imports import is_template_import
from git_code_debt.metrics.imports import PythonImportCount


class TestPythonImports(T.TestCase):

    LINES_TO_EXPECTED = (
        ('import collections', True),
        ('from collections import defaultdict', True),
        ('from foo import bar as baz', True),
        ('import bar as baz', True),
        ('#import foo as bar', False),
        ('from with nothing', False),
        ('    import foo', True),
        ('herpderp', False),
    )

    def test_imports(self):
        for line, expected in self.LINES_TO_EXPECTED:
            T.assert_equal(
                is_python_import(line),
                expected,
            )

class TestTemplateImports(T.TestCase):

    LINES_TO_EXPECTED = (
        ('#import foo', True),
        ('#from foo import bar', True),
        ('#from foo import bar as baz', True),
        ('#import bar as baz', True),
        ('    #import foo', True),
        ('## Nothing to import from here', False),
        ('herpderp', False),
    )

    def test_imports(self):
        for line, expected in self.LINES_TO_EXPECTED:
            T.assert_equal(
                is_template_import(line),
                expected,
            )

class TestPythonImportCount(T.TestCase):

    def test_import_parser(self):
        parser = PythonImportCount()
        input = [
            FileDiffStat(
                'test.py',
                ['import collections', 'from os import path'],
                ['import os.path', 'nothing'],
                None,
            ),
        ]

        metrics = list(parser.get_metrics_from_stat(input))
        T.assert_equal(metrics, [Metric('PythonImportCount', 1)])

class TestCheetahTemplateImportCount(T.TestCase):

    def test_import_parser(self):
        parser = CheetahTemplateImportCount()
        input = [
            FileDiffStat(
                'test.tmpl',
                ['#import collections', '#from os import path'],
                ['#import os.path', 'nothing'],
                None,
            ),
        ]

        metrics = list(parser.get_metrics_from_stat(input))
        T.assert_equal(metrics, [Metric('CheetahTemplateImportCount', 1)])
