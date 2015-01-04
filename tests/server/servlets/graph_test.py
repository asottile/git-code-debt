from __future__ import absolute_import
from __future__ import unicode_literals

import flask
import mock

from git_code_debt.metrics.imports import PythonImportCount
from git_code_debt.metrics.symlink_count import SymlinkCount
from git_code_debt.util import five
from git_code_debt.util.compat import urllib_parse
from testing.assertions.response import assert_no_response_errors
from testing.assertions.response import assert_redirect


def test_all_data(server_with_data):
    resp = server_with_data.server.client.get(flask.url_for(
        'graph.all_data',
        metric_name=PythonImportCount.__name__,
    ))

    # Should redirect to a show url
    assert_redirect(
        resp,
        flask.url_for('graph.show', metric_name=PythonImportCount.__name__),
        # Tested more explicitly below
        mock.ANY,
    )
    # This part is a bit racey due to how the commits were made.
    # Instead of opting for more-exact timing here, I decided to unit test
    # the underlying function and give a fuzzy check here.  The important part
    # about this endpoint is it redirects to a show url and doesn't start at 0
    timestamp = server_with_data.cloneable_with_commits.commits[-1].date
    parsed_qs = urllib_parse.parse_qs(
        urllib_parse.urlparse(resp.response.location).query,
    )
    assert int(parsed_qs['start'][0]) > 0
    assert int(parsed_qs['start'][0]) <= timestamp


def test_all_data_no_data_for_metric(server_with_data):
    resp = server_with_data.server.client.get(flask.url_for(
        'graph.all_data',
        metric_name=SymlinkCount.__name__,
    ))

    # Should redirect to a show url
    assert_redirect(
        resp,
        flask.url_for('graph.show', metric_name=SymlinkCount.__name__),
        {'start': ['0'], 'end': [mock.ANY]},
    )


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


def test_show(server_with_data):
    timestamp = server_with_data.cloneable_with_commits.commits[0].date
    resp = server_with_data.server.client.get(flask.url_for(
        'graph.show',
        metric_name=PythonImportCount.__name__,
        start=five.text(timestamp - 1000),
        end=five.text(timestamp + 1000),
    ))
    assert_no_response_errors(resp)


def test_show_succeeds_for_empty_range(server):
    resp = server.client.get(flask.url_for(
        'graph.show',
        metric_name=PythonImportCount.__name__,
        start='0',
        end='0',
    ))
    assert_no_response_errors(resp)
