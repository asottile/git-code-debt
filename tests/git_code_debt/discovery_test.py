
import testify as T

from git_code_debt.discovery import get_metric_parsers
from git_code_debt.discovery import get_modules
from git_code_debt.discovery import is_metric_cls
from git_code_debt.metrics.base import DiffParserBase
from git_code_debt_util.discovery import discover

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

class MetricParserInTests(DiffParserBase): pass

@T.suite('integration')
class TestGetMetricParsersTest(T.TestCase):

    def test_returns_no_metrics_when_defaults_are_off(self):
        T.assert_equal(set(), get_metric_parsers(include_defaults=False))

    def test_get_metric_parsers_returns_something(self):
        T.assert_gt(len(get_metric_parsers()), 0)

    def test_returns_metrics_defined_in_tests_when_specified(self):
        import tests
        metrics_in_tests = discover(tests, is_metric_cls)
        if not metrics_in_tests:
            raise AssertionError(
                'Expected at least one metric in `tests` but found none'
            )

        T.assert_equal(
            metrics_in_tests,
            get_metric_parsers((tests,), include_defaults=False),
        )

class TestGetModules(T.TestCase):

    def test_get_modules_no_modules(self):
        ret = get_modules([])
        T.assert_equal(ret, [])

    def test_get_modules_some_modules(self):
        ret = get_modules([
            'git_code_debt.metrics', 'git_code_debt.create_tables',
        ])
        # Not a great assertion, but at least it tests that it works
        T.assert_length(ret, 2)
