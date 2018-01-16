from __future__ import absolute_import
from __future__ import unicode_literals

from git_code_debt.discovery import get_metric_parsers
from git_code_debt.discovery import get_modules
from git_code_debt.discovery import is_metric_cls
from git_code_debt.metrics.base import DiffParserBase
from git_code_debt.util.discovery import discover


def test_is_metric_parser_is_DiffParserBase():
    assert not is_metric_cls(DiffParserBase)


def test_is_metric_parser_not_DiffParserBase():
    class Foo(DiffParserBase):
        pass

    assert is_metric_cls(Foo)


def test_is_metric_parser_definitely_isnt_DiffParserBase():
    class Bar(object):
        pass

    assert not is_metric_cls(Bar)


def test_is_metric_parser_is_a_DiffParserBase_but_has__metric__False():
    class Baz(DiffParserBase):
        __metric__ = False
    assert not is_metric_cls(Baz)


class MetricParserInTests(DiffParserBase):
    pass


def test_returns_no_metrics_when_defaults_are_off():
    assert set() == get_metric_parsers(include_defaults=False)


def test_get_metric_parsers_returns_something():
    assert len(get_metric_parsers()) > 0


def test_returns_metrics_defined_in_tests_when_specified():
    import tests
    metrics_in_tests = discover(tests, is_metric_cls)
    if not metrics_in_tests:
        raise AssertionError(
            'Expected at least one metric in `tests` but found none',
        )

    assert (
        metrics_in_tests ==
        get_metric_parsers((tests,), include_defaults=False)
    )


def test_get_modules_no_modules():
    ret = get_modules([])
    assert ret == []


def test_get_modules_some_modules():
    module_names = ['git_code_debt.metrics', 'git_code_debt.generate']
    ret = get_modules(module_names)
    assert len(ret) == 2
    assert [mod.__name__ for mod in ret] == module_names
