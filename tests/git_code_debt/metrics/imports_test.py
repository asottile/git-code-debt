import testify as T

from git_code_debt.metrics.imports import ImportParser
from git_code_debt.metrics.imports import is_python_import
from git_code_debt.metrics.imports import is_template_import
from git_code_debt.diff_parser_base import FileDiffStat
from git_code_debt.metric import Metric


@T.suite('unit')
class ImportParserTest(T.TestCase):

    def test_python_import_check(self):
        T.assert_equal(is_python_import('import collections'), True)
        T.assert_equal(is_python_import('from collections import defaultdict'), True)
        T.assert_equal(is_python_import('from with no followup'), False)
        T.assert_equal(is_python_import('line with nothing related'), False)
        T.assert_equal(is_python_import('line with import not at start'), False)

    def test_template_import_check(self):
        T.assert_equal(is_template_import('#import'), True)
        T.assert_equal(is_template_import('nothing related'), False)
        T.assert_equal(is_template_import('lines with #import not at the beginning'), False)

    def test_import_parser(self):
        parser = ImportParser()
        input = [
            FileDiffStat('test.py', ['import collections', 'from os import path'], ['import os.path', 'nothing'], 'this_should_be_ignored'),
        ]

        metrics = [item for item in parser.get_metrics_from_stat(input)]
        T.assert_equal(metrics, [
            Metric('ImportCount_Python', 1),
            Metric('ImportCount_Template', 0),
        ])