
import __builtin__

import mock
import pytest

from git_code_debt.list_metrics import color
from git_code_debt.list_metrics import CYAN
from git_code_debt.list_metrics import main
from git_code_debt.list_metrics import NORMAL


# pylint:disable=redefined-outer-name


@pytest.yield_fixture
def print_mock():
    with mock.patch.object(__builtin__, 'print', autospec=True) as print_mock:
        yield print_mock


@pytest.mark.integration
def test_list_metrics_smoke(print_mock):
    # This test is just to make sure that it doesn't fail catastrophically
    main([])
    assert print_mock.called


@pytest.mark.integration
def test_list_metrics_no_color_smoke(print_mock):
    main(['--color', 'never'])
    assert all([
        '\033' not in call[0][0] for call in print_mock.call_args_list
    ])


def test_color_no_color():
    ret = color('foo', 'bar', False)
    assert ret == 'foo'


def test_colored():
    ret = color('foo', CYAN, True)
    assert ret == CYAN + 'foo' + NORMAL
