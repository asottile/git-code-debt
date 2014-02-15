
import testify as T

from testing.base_classes.test import test
from testing.utilities.testing_response import TestingResponse
from testing.utilities.auto_namedtuple import auto_namedtuple


@test
def test_ctor():
    response = object()
    instance = TestingResponse(response)
    T.assert_equal(instance.response, response)

@test
def test_pq():
    response = auto_namedtuple('Response', data='<p>Oh hai!</p>')
    instance = TestingResponse(response)
    T.assert_equal(instance.pq.__html__(), response.data)

@test
def test_json():
    response = auto_namedtuple('Response', data='{"foo": "bar"}')
    instance = TestingResponse(response)
    T.assert_equal(instance.json, {'foo': 'bar'})
