
import testify as T

from testing.base_classes.flask_test_case import FlaskTestCase
from git_code_debt_server.app import app

@T.suite('integration')
class GitCodeDebtServerTestCase(FlaskTestCase):
    __test__ = False

    FLASK_APPLICATION = app
