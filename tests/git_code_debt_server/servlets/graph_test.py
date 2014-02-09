
import flask
import testify as T
import urlparse

from git_code_debt.metrics.imports import PythonImportCount
from testing.assertions.response import assert_no_response_errors
from testing.base_classes.git_code_debt_server_test_case import GitCodeDebtServerWithDataTestCase


class GraphTest(GitCodeDebtServerWithDataTestCase):
    def test_all_data(self):
        resp = self.client.get(flask.url_for(
            'graph.all_data',
            metric_name=PythonImportCount.__name__,
        ))

        # Should redirect to a show url
        T.assert_equal(resp.response.status_code, 302)
        parsed = urlparse.urlparse(resp.response.location)
        T.assert_equal(
            parsed.path,
            flask.url_for('graph.show', metric_name=PythonImportCount.__name__),
        )
        parsed_qs = urlparse.parse_qs(parsed.query)
        T.assert_equal(parsed_qs['start'], ['1384445142'])

    def test_show(self):
        resp = self.client.get(flask.url_for(
            'graph.show',
            metric_name=PythonImportCount.__name__,
            start='1384445142',
            end='1385445142',
        ))
        assert_no_response_errors(resp)
