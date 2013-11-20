
import testify as T

from git_code_debt.metrics.base import DiffParserBase
from git_code_debt.discovery import get_metric_parsers
from git_code_debt.discovery import is_metric_cls

class TestIsMetricCls(T.TestCase):

    def test_not_DiffParserBase(self):
        T.assert_is(is_metric_cls(DiffParserBase), False)

    def test_is_DiffParserBase(self):
         class Foo(DiffParserBase): pass
         T.assert_is(is_metric_cls(Foo), True)

    def test_definitely_isnt_DiffParserBase(self):
        class Bar(object): pass
        T.assert_is(is_metric_cls(Bar), False)

    def test_is_a_DiffParserBase_but_has__metric__False(self):
        class Baz(DiffParserBase):
            __metric__ = False
        T.assert_is(is_metric_cls(Baz), False)

@T.suite('integration')
class TestGetMetricParsersSmokeTest(T.TestCase):

    def test_get_metric_parsers_returns_something(self):
        T.assert_gt(len(get_metric_parsers()), 0)
