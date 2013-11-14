
import flask.testing
import mock
import testify as T

from testing.utilities.testing_client import TestingClient
from testing.utilities.testing_response import TestingResponse

class TestTestingClient(T.TestCase):

    @T.setup_teardown
    def patch_out_base_open_method(self):
        with mock.patch.object(
            flask.testing.FlaskClient, 'open', autospec=True,
        ) as self.open_mock:
            yield

    def test_patch_ip_sends_along_ip(self):
        instance = TestingClient(None)
        remote_addr = object()
        with instance.patch_ip(remote_addr):
            instance.open('/')
            self.open_mock.assert_called_once_with(
                instance,
                '/',
                environ_base={'REMOTE_ADDR': remote_addr},
            )

    def test_takes_environment(self):
        instance = TestingClient(None)
        environ_base = {'foo': 'bar'}
        instance.open('/', environ_base=environ_base)
        self.open_mock.assert_called_once_with(
            instance,
            '/',
            environ_base=environ_base,
        )

    def test_return_value_is_testing_response(self):
        instance = TestingClient(None)
        ret = instance.open('/')
        T.assert_isinstance(ret, TestingResponse)

