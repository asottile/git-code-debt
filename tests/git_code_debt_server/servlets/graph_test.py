
import flask
import mock
import pytest

from git_code_debt.metrics.imports import PythonImportCount
from testing.assertions.response import assert_no_response_errors
from testing.assertions.response import assert_redirect


@pytest.mark.integration
def test_all_data(server_with_data):
    resp = server_with_data.server.client.get(flask.url_for(
        'graph.all_data',
        metric_name=PythonImportCount.__name__,
    ))

    # Should redirect to a show url
    timestamp = server_with_data.cloneable_with_commits.commits[0].date
    assert_redirect(
        resp,
        flask.url_for('graph.show', metric_name=PythonImportCount.__name__),
        {
            'start': [unicode(timestamp)],
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
    timestamp = server_with_data.cloneable_with_commits.commits[0].date
    resp = server_with_data.server.client.get(flask.url_for(
        'graph.show',
        metric_name=PythonImportCount.__name__,
        start=unicode(timestamp - 1000),
        end=unicode(timestamp + 1000),
    ))
    assert_no_response_errors(resp)


@pytest.mark.integration
def test_show_succeeds_for_empty_range(server):
    resp = server.client.get(flask.url_for(
        'graph.show',
        metric_name=PythonImportCount.__name__,
        start='0',
        end='0',
    ))
    assert_no_response_errors(resp)
