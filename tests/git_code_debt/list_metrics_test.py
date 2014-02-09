
import __builtin__

import mock
import testify as T

from git_code_debt.list_metrics import color
from git_code_debt.list_metrics import CYAN
from git_code_debt.list_metrics import main
from git_code_debt.list_metrics import NORMAL
from testing.base_classes.test import test


@T.suite('integration')
class TestListMetricsSmoke(T.TestCase):
    def test_smoke(self):
        # This test is just to make sure that it doesn't fail catastrophically
        with mock.patch.object(__builtin__, 'print', autospec=True) as print_mock:
            main([])
            T.assert_true(print_mock.called)


@test
def test_color_no_color():
    ret = color('foo', 'bar', False)
    T.assert_equal(ret, 'foo')


@test
def test_colored():
    ret = color('foo', CYAN, True)
    T.assert_equal(ret, CYAN + 'foo' + NORMAL)
