
import flask
import testify as T

from git_code_debt_server.servlets.index import DeltaPresenter
from testing.assertions.response import assert_no_response_errors
from testing.base_classes.git_code_debt_server_test_case import GitCodeDebtServerTestCase
from testing.base_classes.git_code_debt_server_test_case import GitCodeDebtServerWithDataTestCase
from testing.base_classes.test import test


class TestIndexLoadsMixin(object):
    def test_index_loads(self):
        response = self.client.get(flask.url_for('index.show'))
        assert_no_response_errors(response)


class TestIndexNoData(GitCodeDebtServerTestCase, TestIndexLoadsMixin): pass
class TestIndex(GitCodeDebtServerWithDataTestCase, TestIndexLoadsMixin): pass


@test
def test_delta_classname_negative():
    delta = DeltaPresenter('url', -9001)
    T.assert_equal(delta.classname, 'metric-down')

@test
def test_delta_classname_zero():
    delta = DeltaPresenter('url', 0)
    T.assert_equal(delta.classname, 'metric-none')

@test
def test_delta_classname_positive():
    delta = DeltaPresenter('url', 9001)
    T.assert_equal(delta.classname, 'metric-up')
