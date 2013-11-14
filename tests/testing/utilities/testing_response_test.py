
import testify as T

from testing.utilities.testing_response import TestingResponse
from util.auto_namedtuple import auto_namedtuple

class TestTestingResponse(T.TestCase):

    def test_ctor(self):
        response = object()
        instance = TestingResponse(response)
        T.assert_equal(instance.response, response)

    def test_pq(self):
        response = auto_namedtuple('Response', data='<p>Oh hai!</p>')
        instance = TestingResponse(response)
        T.assert_equal(instance.pq.__html__(), response.data)

    def test_json(self):
        response = auto_namedtuple('Response', data='{"foo": "bar"}')
        instance = TestingResponse(response)
        T.assert_equal(instance.json, {'foo': 'bar'})
