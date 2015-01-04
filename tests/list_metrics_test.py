# pylint:disable=redefined-outer-name
from __future__ import absolute_import
from __future__ import unicode_literals

import mock
import pytest

from git_code_debt.list_metrics import color
from git_code_debt.list_metrics import CYAN
from git_code_debt.list_metrics import main
from git_code_debt.list_metrics import NORMAL
from git_code_debt.util.compat import builtins


@pytest.yield_fixture
def print_mock():
    with mock.patch.object(builtins, 'print') as print_mock:
        yield print_mock


def test_list_metrics_smoke(print_mock):
    # This test is just to make sure that it doesn't fail catastrophically
    main([])
    assert print_mock.called


def test_list_metrics_no_color_smoke(print_mock):
    main(['--color', 'never'])
    calls_args = [call[0][0] for call in print_mock.call_args_list]
    assert all(['\033' not in calls_args])


def test_color_no_color():
    ret = color('foo', 'bar', False)
    assert ret == 'foo'


def test_colored():
    ret = color('foo', CYAN, True)
    assert ret == CYAN + 'foo' + NORMAL
