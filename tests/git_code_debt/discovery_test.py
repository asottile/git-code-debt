
import testify as T

from git_code_debt.diff_parser_base import DiffParserBase
from git_code_debt.discovery import is_metric_cls

class TestIsMetricCls(T.TestCase):

    def test_not_DiffParserBase(self):
        T.assert_equal(False, is_metric_cls(DiffParserBase))

    def test_is_DiffParserBase(self):
         class Foo(DiffParserBase): pass
         T.assert_equal(True, is_metric_cls(Foo))

    def test_definitely_isnt_DiffParserBase(self):
        class Bar(object): pass
        T.assert_equal(False, is_metric_cls(Bar))
