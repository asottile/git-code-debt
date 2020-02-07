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
    response = auto_namedtuple(
        'Response', data=b'<p>Oh hai!</p>', charset='UTF-8',
    )
    instance = Response(response)
    assert instance.pq.__html__() == response.data.decode('UTF-8')


def test_json():
    response = auto_namedtuple(
        'Response', data=b'{"foo": "bar"}', charset='UTF-8',
    )
    instance = Response(response)
    assert instance.json == {'foo': 'bar'}
