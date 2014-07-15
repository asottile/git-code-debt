from __future__ import absolute_import
from __future__ import unicode_literals

from git_code_debt.server.presentation.delta import DeltaPresenter


def test_delta_classname_negative():
    delta = DeltaPresenter('url', -9001)
    assert delta.classname == 'metric-down'


def test_delta_classname_zero():
    delta = DeltaPresenter('url', 0)
    assert delta.classname == 'metric-none'


def test_delta_classname_positive():
    delta = DeltaPresenter('url', 9001)
    assert delta.classname == 'metric-up'
