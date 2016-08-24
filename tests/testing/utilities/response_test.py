from __future__ import absolute_import
from __future__ import unicode_literals

from testing.utilities.auto_namedtuple import auto_namedtuple
from testing.utilities.response import Response


def test_ctor():
    response = object()
    instance = Response(response)
    assert instance.response == response


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
