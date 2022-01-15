from __future__ import annotations

from git_code_debt.server.presentation.delta import Delta


def test_delta_classname_negative():
    delta = Delta('url', -9001)
    assert delta.classname == 'metric-down'


def test_delta_classname_zero():
    delta = Delta('url', 0)
    assert delta.classname == 'metric-none'


def test_delta_classname_positive():
    delta = Delta('url', 9001)
    assert delta.classname == 'metric-up'
