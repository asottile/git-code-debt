from __future__ import annotations

from unittest import mock

import flask.testing
import pytest

from testing.utilities.auto_namedtuple import auto_namedtuple
from testing.utilities.client import Client
from testing.utilities.client import Response


@pytest.fixture
def client_open_mock():
    with mock.patch.object(flask.testing.FlaskClient, 'open') as open_mock:
        yield open_mock


def test_return_value_is_testing_response(client_open_mock):
    instance = Client(None)
    ret = instance.open('/')
    assert isinstance(ret, Response)


def test_pq():
    response = auto_namedtuple('Response', text='<p>Oh hai!</p>')
    instance = Response(response)
    assert instance.pq.__html__() == response.text


def test_json():
    response = auto_namedtuple('Response', text='{"foo": "bar"}')
    instance = Response(response)
    assert instance.json == {'foo': 'bar'}
