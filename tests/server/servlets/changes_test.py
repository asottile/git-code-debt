from __future__ import absolute_import
from __future__ import unicode_literals

import flask
import pyquery

from testing.assertions.response import assert_no_response_errors


def test_changes_endpoint(server_with_data):
    resp = server_with_data.server.client.get(flask.url_for(
        'changes.show',
        metric_name='PythonImportCount',
        start_timestamp=0,
        # Some sufficiently large number to include all the data
        end_timestamp=2 ** 62,
    ))
    assert_no_response_errors(resp)
    pq = pyquery.PyQuery(resp.json['body'])
    # Should have a table in output
    assert len(pq.find('table')) == 1
    # Should show the metric went up by 2
    assert pq.find('.metric-up').text() == '2'
