
import flask
import pytest
import urlparse

from git_code_debt.metrics.imports import PythonImportCount
from testing.assertions.response import assert_no_response_errors


@pytest.mark.integration
def test_all_data(server_with_data):
    resp = server_with_data.client.get(flask.url_for(
        'graph.all_data',
        metric_name=PythonImportCount.__name__,
    ))

    # Should redirect to a show url
    assert resp.response.status_code == 302
    parsed = urlparse.urlparse(resp.response.location)
    assert (
        parsed.path ==
        flask.url_for('graph.show', metric_name=PythonImportCount.__name__),
    )
    parsed_qs = urlparse.parse_qs(parsed.query)
    assert parsed_qs['start'] == ['1384445142']


@pytest.mark.integration
def test_show(server_with_data):
    resp = server_with_data.client.get(flask.url_for(
        'graph.show',
        metric_name=PythonImportCount.__name__,
        start='1384445142',
        end='1385445142',
    ))
    assert_no_response_errors(resp)
