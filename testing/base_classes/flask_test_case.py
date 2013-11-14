
import contextlib
import mock
import testify as T

from testing.utilities.testing_client import TestingClient

class FlaskTestCase(T.TestCase):
    """A Flask test case provides the basics for testing a flask application."""
    __test__ = False

    FLASK_APPLICATION = None

    @T.setup_teardown
    def setup_flask_app_instance(self):
        """Sets up a test client instance for use in testing."""
        # Patch in our own test client class
        with contextlib.nested(
            mock.patch.object(
                self.FLASK_APPLICATION,
                'test_client_class',
                TestingClient,
            ),
            # Make the app always debug so it throws exceptions
            mock.patch.object(
                type(self.FLASK_APPLICATION),
                'debug',
                mock.PropertyMock(return_value=True),
            ),
        ):
            with contextlib.nested(
                self.FLASK_APPLICATION.test_request_context(),
                self.FLASK_APPLICATION.test_client(),
            ) as (
                self.request_context,
                self.client,
            ):
                yield
