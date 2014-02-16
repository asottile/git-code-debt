
import flask
import mock
import pytest

from git_code_debt.metrics.imports import PythonImportCount
from testing.assertions.response import assert_no_response_errors
from testing.assertions.response import assert_redirect


@pytest.mark.integration
def test_all_data(server_with_data):
    resp = server_with_data.client.get(flask.url_for(
        'graph.all_data',
        metric_name=PythonImportCount.__name__,
    ))

    # Should redirect to a show url
    assert_redirect(
        resp,
        flask.url_for('graph.show', metric_name=PythonImportCount.__name__),
        {
            'start': ['1384445142'],
            'end': [mock.ANY],
        },
    )


@pytest.mark.integration
def test_all_data_no_data(server):
    resp = server.client.get(flask.url_for(
        'graph.all_data',
        metric_name=PythonImportCount.__name__,
    ))

    # Should redirect to start of 0
    assert_redirect(
        resp,
        flask.url_for('graph.show', metric_name=PythonImportCount.__name__),
        {
            'start': ['0'],
            'end': [mock.ANY],
        },
    )


@pytest.mark.integration
def test_show(server_with_data):
    resp = server_with_data.client.get(flask.url_for(
        'graph.show',
        metric_name=PythonImportCount.__name__,
        start='1384445142',
        end='1385445142',
    ))
    assert_no_response_errors(resp)
