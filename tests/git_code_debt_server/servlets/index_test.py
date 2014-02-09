
import flask

from testing.assertions.response import assert_no_response_errors
from testing.base_classes.git_code_debt_server_test_case import GitCodeDebtServerTestCase
from testing.base_classes.git_code_debt_server_test_case import GitCodeDebtServerWithDataTestCase


class TestIndexLoadsMixin(object):
    def test_index_loads(self):
        response = self.client.get(flask.url_for('index.show'))
        assert_no_response_errors(response)


class TestIndexNoData(GitCodeDebtServerTestCase, TestIndexLoadsMixin): pass
class TestIndex(GitCodeDebtServerWithDataTestCase, TestIndexLoadsMixin): pass


