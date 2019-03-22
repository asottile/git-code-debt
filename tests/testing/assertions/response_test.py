from __future__ import absolute_import
from __future__ import unicode_literals

import mock
import pytest

from testing.assertions.response import assert_no_response_errors
from testing.assertions.response import assert_redirect
from testing.utilities.auto_namedtuple import auto_namedtuple


def test_raises_for_response_error():
    with pytest.raises(AssertionError):
        assert_no_response_errors(
            auto_namedtuple(response=auto_namedtuple(status_code=201)),
        )


def test_ok_for_200():
    assert_no_response_errors(
        auto_namedtuple(response=auto_namedtuple(status_code=200)),
    )


def test_redirect_not_a_redirect():
    with pytest.raises(AssertionError):
        assert_redirect(
            auto_namedtuple(response=auto_namedtuple(status_code=200)),
            mock.sentinel.expected_path,
            mock.sentinel.expected_query,
        )


def test_redirect_custom_status_code():
    assert_redirect(
        auto_namedtuple(
            response=auto_namedtuple(
                status_code=303,
                location='/foo',
            ),
        ),
        '/foo',
        {},
        redirect_status_code=303,
    )


def test_redirect_wrong_path():
    with pytest.raises(AssertionError):
        assert_redirect(
            auto_namedtuple(
                response=auto_namedtuple(
                    status_code=302,
                    location='/foo',
                ),
            ),
            '/bar',
            {},
        )


def test_redirect_wrong_query():
    with pytest.raises(AssertionError):
        assert_redirect(
            auto_namedtuple(
                response=auto_namedtuple(
                    status_code=302,
                    location='/foo?bar=baz',
                ),
            ),
            '/foo',
            {'bar': ['biz']},
        )


def test_correct_redirect():
    assert_redirect(
        auto_namedtuple(
            response=auto_namedtuple(
                status_code=302,
                location='/foo?bar=baz',
            ),
        ),
        '/foo',
        {'bar': ['baz']},
    )
