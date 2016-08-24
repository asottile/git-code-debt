from __future__ import absolute_import
from __future__ import unicode_literals

import flask.testing
import mock
import pytest

from testing.utilities.client import Client
from testing.utilities.response import Response


@pytest.yield_fixture
def client_open_mock():
    with mock.patch.object(flask.testing.FlaskClient, 'open') as open_mock:
        yield open_mock


def test_patch_ip_sends_along_ip(client_open_mock):
    instance = Client(None)
    remote_addr = object()
    with instance.patch_ip(remote_addr):
        instance.open('/')
        client_open_mock.assert_called_once_with(
            '/',
            environ_base={'REMOTE_ADDR': remote_addr},
        )


def test_takes_environment(client_open_mock):
    instance = Client(None)
    environ_base = {'foo': 'bar'}
    instance.open('/', environ_base=environ_base)
    client_open_mock.assert_called_once_with(
        '/',
        environ_base=environ_base,
    )


def test_return_value_is_testing_response(client_open_mock):
    instance = Client(None)
    ret = instance.open('/')
    assert isinstance(ret, Response)
