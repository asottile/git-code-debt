from __future__ import absolute_import
from __future__ import unicode_literals

from testing.utilities.auto_namedtuple import auto_namedtuple
from testing.utilities.response import Response


def test_ctor():
    response = object()
    instance = Response(response)
    assert instance.response == response


def test_pq():
    response = auto_namedtuple('Response', data='<p>Oh hai!</p>')
    instance = Response(response)
    assert instance.pq.__html__() == response.data


def test_json():
    response = auto_namedtuple('Response', data='{"foo": "bar"}')
    instance = Response(response)
    assert instance.json == {'foo': 'bar'}
