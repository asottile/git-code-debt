
import __builtin__

import mock
import pytest

from git_code_debt.list_metrics import color
from git_code_debt.list_metrics import CYAN
from git_code_debt.list_metrics import main
from git_code_debt.list_metrics import NORMAL


@pytest.mark.integration
def test_list_metricssmoke():
    # This test is just to make sure that it doesn't fail catastrophically
    with mock.patch.object(__builtin__, 'print', autospec=True) as print_mock:
        main([])
        assert print_mock.called


def test_color_no_color():
    ret = color('foo', 'bar', False)
    assert ret == 'foo'


def test_colored():
    ret = color('foo', CYAN, True)
    assert ret == CYAN + 'foo' + NORMAL
